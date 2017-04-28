from django.utils import timezone
from django.template.loader import get_template

from game import loader
from game.models import Village, Event

def create_event(village, eventtype, time=None):
    if (time is None):
        time = timezone.now()

    context = eventtype(village)

    return Event.create(hometown = village,
                 eventtype = eventtype,
                 context = context,
                 time = time)

def create_event_by_textid(village, textid, time=None):
    return create_event(village, village.get_ruleset().get_eventtype(textid), time)

def get_message(event):
    eventtype = event.hometown.get_ruleset().get_eventtype(event.textid)
    msg = get_template(eventtype.template).render(event.get_context())
    
    return msg 
