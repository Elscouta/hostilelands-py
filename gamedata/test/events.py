from __future__ import division

from game.exceptions import *

from .ruleset import ruleset

@ruleset.EventType_Declare('basicevent', 'basicevent.txt')
def basicevent(village):
    return {}

@ruleset.EventType_Declare('templatedevent', 'templatedevent.txt')
def templatedevent(village):
    return { 'data': 'value' }

@ruleset.EventType_Declare('birth', 'birth.txt')
def birth(village):
    village.add_res("population", 1)

    return {}

@ruleset.EventType_Declare('starvation', 'starvation.txt')
def starvation(village):
    population = village.get_res_total("population")

    if (population > 15):
        deaths = int(population / 3)
    elif (population > 12):
        deaths = 4
    elif (population > 10):
        deaths = 3
    elif (population > 8):
        deaths = 2
    else:
        deaths = 1

    village.add_res("population", -deaths)

    while (village.get_res_production("food") < 0):
        if (village.get_res_total("population") < 0):
            raise UnexpectedState("The village completely died!")

        deaths += 1
        village.add_res("population", -1)

    return { "deaths": deaths }
