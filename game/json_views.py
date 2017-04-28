from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse,Http404

from json import loads as json_load
from json import dumps as json_dump

from game import models, properties, events
from game import building
from game.villages import open_village
from game.httputils import json_handler

@json_handler
def storage(request, village_id):
    village = open_village(village_id)
    
    response = {}
    for res,restype in village.get_ruleset().get_all_ressourcetypes().items():
        if (village.get_res_total(res) == 0):
            continue
        
        response[res] = { 'current': float(village.get_res_total(res)),
                          'production': float(village.get_res_production(res)),
                          'free': float(village.get_res_free(res)),
                          'storage': float(village.get_res_storage(res)),
                          'nouse' : restype.has_tag("nouse"),
                          'noprod' : restype.has_tag("noprod"),
                          'integer': restype.has_tag("integer"),
                          'category': restype.get_category() }

    return { "value" : response }



@json_handler
def building_list(request, village_id):
    village = open_village(village_id)

    buildinglist = building.Building.objects.filter(hometown=village_id)
    response = []

    for bld in buildinglist:
        bld_data = village.get_ruleset().get_all_buildingtypes()[bld.textid]
        assert(bld_data.textid == bld.textid)

        response.append({ "textid": bld_data.textid,
                          "name" : bld_data.name,
                          "level" : bld.level });

    return { "value": response }



@json_handler
def get_property(request, village_id, propid):
    village = open_village(village_id)

    if (not propid in village.get_ruleset().get_all_propertytypes()):
        raise Http404("Unknown property type")

    return { "value" : float(village.get_property_value(propid)) }


@csrf_exempt
@json_handler
def set_property(request, village_id, propid):
    village = open_village(village_id)

    value = json_load(request.body.decode("ascii"))['value'];
        
    proptype = village.get_ruleset().get_propertytype(propid)

    village.set_property_value(propid, properties.validate_input(proptype, value))

    return { }

@json_handler
def get_event(request, village_id, event_id):
    village = open_village(village_id)
    event = get_object_or_404(models.Event, pk=event_id, hometown=village_id)

    msg = events.get_message(event)

    return { "value": msg }

@json_handler
def list_unread_events(request, village_id):
    village = get_object_or_404(models.Village, pk=village_id)

    unread_events = models.Event.objects.filter(hometown=village_id, unread=True)
    unread_ids = [ e.pk for e in unread_events ]

    return { "value" : unread_ids }

@json_handler
def mark_event_read(request, village_id, event_id):
    event = get_object_or_404(models.Event, pk=event_id, hometown=village_id)
    event.mark_read()

    return { }
