from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.urlresolvers import reverse

from .models import Village

def rename(request, village_id):
    village = get_object_or_404(Village, pk=village_id)
    try:
        village.name = request.POST['newname']
        village.save()
    except (KeyError):
        return HttpResponse("", status=404)
    else:
        return HttpResponseRedirect(reverse('village', args=(village_id,)))


def reset(request, village_id):
    pass
