from decimal import Decimal
import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone 

from game import tasks, events, loader
from game.models import Village

# Creates an empty village
def create_village(name):
    v = Village(name=name, simulation_time = timezone.now())
    v.save()
    
    loader.get_ruleset().init_village(v)
    return v


def yield_ressources_simulation_handlers(village, time_elapsed):
    assert(time_elapsed > 0)

    for resid,restype in village.get_ruleset().get_all_ressourcetypes().items():
        
        res = restype.get_textid()
        
        if (restype.has_tag("noprod")):
            assert(village.get_res_production(res) == 0)
            continue
        
        prod = village.get_res_production(res)

        ##
        # Handles the normal consumption/production of ressources
        #
        def ressource_handler(timegap, restype=restype, prod=prod):
            village.add_res(restype.get_textid(), timegap * prod)

        
        if (village.get_res_total(res) + prod * time_elapsed < 0):
            ##
            # Handles the ressource becoming negative through the registered
            # signal.
            #
            # Note: Handler failing to handle the event will cause general
            # mayhem
            #
            def negative_handler(endpoint, restype=restype):

                if (restype.on_negative == None):
                    raise UnexpectedState('Unable to handle negative ressource')

                events.create_event_by_textid(village, restype.on_negative, endpoint)

                if (village.get_res_production(restype.get_textid()) < 0):
                    raise UnexpectedState('Unable to handle negative ressource (after firing handler)')

            newtimegap = - village.get_res_total(res) / prod
            yield (newtimegap, ressource_handler, negative_handler)

        
        else:
            
            yield (time_elapsed, ressource_handler, None)

def yield_tasks_simulation_handlers(village, time_elapsed):
    def tasks_handler(timegap):
        tasks.advance_tasks(village, timegap)
    
    yield (time_elapsed, tasks_handler, None)


def yield_events_simulation_handlers(village, time_elapsed):
    return
    yield


def yield_simulation_handlers(village, time_elapsed):
    for hdl in yield_ressources_simulation_handlers(village, time_elapsed):
        yield hdl

    for hdl in yield_tasks_simulation_handlers(village, time_elapsed):
        yield hdl

    for hdl in yield_events_simulation_handlers(village, time_elapsed):
        yield hdl
            
## 
# Simulates the village from the last time this function was called to the current time
# Should be called every time before an action changing ressource production occurs.
# Saves the village to database.
#
# This won't perform anything if a simulation was performed in the last second.
def simulate(village):
    newsimulation_time = timezone.now()

    forceadvance_delta = Decimal('0.05')
   
    while (True):
        time_elapsed = Decimal((newsimulation_time - village.simulation_time).total_seconds())
        if (time_elapsed < 1):
            return

        hdlrs = list(yield_simulation_handlers(village, time_elapsed))

        min_timegap = time_elapsed
        min_endpoint_hdlr = None
        for (timegap, timegap_hdlr, endpoint_hdlr) in hdlrs:
            if (timegap < min_timegap):
                min_timegap = timegap
                min_endpoint_hdlr = endpoint_hdlr

        # Security to make sure the server dosn't hang in case of a buggy config
        if (min_timegap < forceadvance_delta):
            min_timegap = forceadvance_delta

        for (timegap, timegap_hdlr, endpoint_hdlr) in hdlrs:
            timegap_hdlr(min_timegap)

        endpoint = village.simulation_time + datetime.timedelta(seconds = float(min_timegap))
        village.simulation_time = endpoint
        
        if (not min_endpoint_hdlr is None):
            min_endpoint_hdlr(endpoint)

        village.save()

        forceadvance_delta *= 2

# Simulates the village on open
def open_village(village_id):
    village = get_object_or_404(Village, pk=village_id)
    simulate(village)

    return village
