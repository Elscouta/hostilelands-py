from django.shortcuts import render, get_object_or_404
from django.db import models, transaction
from django.http import HttpResponse,Http404,JsonResponse

import re

from game.exceptions import *
from game.models import Village,Task
from gamedata.common.utils import merge_costs

def start_task(village, tasktype):
    if (not village.has_available_res(merge_costs(tasktype.get_cost(), tasktype.get_uses()))):
        raise InsufficientRessourcesViolation("Can't start task. ",
                                          village,
                                          costs = tasktype.get_cost(), 
                                          uses = tasktype.get_uses())

    if (not village.has_reqs(tasktype.get_reqs())):
        raise GameRulesViolation("You don't fulfill the requirements.");
    
    if (tasktype.is_unique() is True and village.has_task(tasktype.get_base_textid())):
        raise GameRulesViolation("This task has already been started.");
            
    t = Task.create(village, tasktype)
    village.pay_res(tasktype.get_cost())
    village.commit_res(tasktype.get_uses(), t)

def start_task_by_textid(village, textid):
    tasktype = village.get_ruleset().get_tasktype(textid)
    start_task(village, tasktype)
            
def complete_task(task):
    if (not task.is_finished()):
        raise GameRulesViolation("This task has not finished yet! Current completion is {} of {}",
                                 task.completion, task.length)

    if (task.is_continuous()):
        raise GameRulesViolation("This task is continuous and can't be completed.")

    tasktype = task.hometown.get_ruleset().get_tasktype(task.get_textid())
    response_msg = tasktype.collect_rewards(task.hometown)
    
    remove_task(task)

    return response_msg

def update_task(task, params):
    if (not task.is_continuous()):
        raise GameRulesViolation("Only continuous tasks can be modified.")

    tasktype = task.hometown.get_ruleset().get_tasktype_altered(task.get_textid(), params)

    task.hometown.free_res(task)
    
    if (not task.hometown.has_available_res(tasktype.get_uses())):
        raise InsufficientRessourcesViolation("Can't update this task. ", 
                                              task.hometown, 
                                              uses=tasktype.get_uses())
    
    task.hometown.commit_res(tasktype.get_uses(), task)
    task.set_params(tasktype.get_params())
    task.save()

def remove_task(task):
    task.hometown.free_res(task)
    task.delete()

# Advance tasks of the village by the given time.
def advance_tasks(village, time_elapsed):
    tasks = Task.objects.filter(hometown=village.pk)
    work_multiplier = village.get_property_value('property:work_multiplier')
    tasks.update(completion = models.F('completion') + time_elapsed * work_multiplier)


