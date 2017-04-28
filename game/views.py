from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache
from django.template import RequestContext, loader
from django.http import HttpResponse,Http404,JsonResponse

from . import tasks
from game.models import Village
from game.building import Building
from game.loader import get_ruleset

def get_building_or_404(building_name):
    try:
        return get_ruleset().get_buildingtype(building_name)
    except (KeyError):
        raise Http404("There is no such building!")

# Create your views here.
def index(request):
    village_list = Village.objects.order_by('-id')[:5]
    context = { 'village_list': village_list }
    return render(request, 'game/index.html', context)

def village(request, village_id):
    village = get_object_or_404(Village, pk=village_id)

    context = { 'village': village }

    return render(request, 'game/village.html', context)


def building_show(request, village_id, building_textid):
    village = get_object_or_404(Village, pk=village_id)
    building = get_object_or_404(Building, hometown=village_id, textid=building_textid)

    context = { 'village': village,
                'building': building }
    
    return render(request, building.get_template_view(), context)


def manager_tasks(request, village_id):
    village = get_object_or_404(Village, pk=village_id)

    context = { 'village': village }

    return render(request, "game/manager/tasks.html", context)
