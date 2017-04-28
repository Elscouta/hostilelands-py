from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse,Http404

from game import tasks
from game.httputils import json_handler
from game.models import Village, Task
from game.villages import open_village

@json_handler
def start(request, village_id, task_textid):
    village = open_village(village_id)
    
    tasktype = village.get_ruleset().get_tasktype(task_textid)

    tasks.start_task(village, tasktype)

    return {}


@json_handler
def end(request, village_id, task_id):
    village = open_village(village_id)

    task = get_object_or_404(Task, hometown=village_id, pk=task_id)

    response_msg = tasks.complete_task(task)
        
    return { 'msg': response_msg }



@json_handler
def cancel(request, village_id, task_id):
    village = open_village(village_id)

    task = get_object_or_404(Task, hometown=village_id, pk=task_id)

    tasks.remove_task(task)

    return {  }



@json_handler
def addworker(request, village_id, task_id):
    village = open_village(village_id)
    task = get_object_or_404(Task, pk=task_id)

    workers = Decimal(task.get_param("workers"))
    assert(workers == int(workers))

    tasks.update_task(task, { "workers" : workers + 1 })

    return { }
        


@json_handler
def removeworker(request, village_id, task_id):
    village = open_village(village_id)
    task = get_object_or_404(Task, pk=task_id)

    workers = Decimal(task.get_param("workers"))
    assert(workers == int(workers))

    if (workers <= 1):
        tasks.remove_task(task)
        
    else:
        tasks.update_task(task, { "workers" : workers - 1 })

    return {}
   


@json_handler
def active_task_list(request, village_id, enctags):
    village = open_village(village_id)

    tasklist = Task.objects.filter(hometown=village_id)
    response = []
    tags = enctags.split('+')
    for task in tasklist:
        task_type = village.get_ruleset().get_tasktype(task.get_textid())

        if (task_type.has_all_tags(tags)):
            response.append({ "id": task.pk,
                              "textid": task.get_textid(),
                              "shortdesc": task_type.get_shortdesc(),
                              "current_completion": float(task.get_current_completion()),
                              "completion_speed": float(village.get_property_value('property:work_multiplier')),
                              "is_continuous": task.is_continuous(),
                              "length": task.length })


    return { "value" : response }



# Returns the tasks that the village can potentially perform (takes
# into account requirements, but not costs)
# The return value is a dictionnary in tasktype-for-user format
@json_handler
def possible_task_list(request, village_id, enctags):
    village = open_village(village_id)

    required_tags = enctags.split('+')
    possible_tasks = []

    for taskname,tasktemplate in village.get_ruleset().get_all_tasktemplates().items():

        tasktype = tasktemplate.for_village(village)
    
        if (not tasktype.has_all_tags(required_tags)):
            continue
            
        if (not village.has_reqs(tasktype.get_reqs())):
            continue
            
        if (tasktype.is_unique() and village.has_task(tasktype.get_base_textid())):
            continue
          
        possible_tasks.append({ 'textid': tasktype.get_textid(),
                                'cost': tasktype.get_cost(),
                                'shortdesc': tasktype.get_shortdesc(),
                                'longdesc': tasktype.get_longdesc(village)})

    return { "value" : possible_tasks }

