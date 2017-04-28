from gamedata.common.keywords import *

from .ruleset import ruleset

# Convinces a couple of people to join the village. The
# success of this expedition depends of the amount of food
# lying around (or not)
@ruleset.TaskType_Exp_Define
class ConvinceColons:
    textid = "convincecolons"
    popsize = 0
    length = 3
    shortdesc = "Convince additional colons to join you"
    effectdesc = "Increases population by 1"
    reqs = { "building:townhall" : greater(1),
             "building:huts" : greater(1) }

    def collect_rewards(village):
        village.add_res('population', 1)
        return "A lone farmer is glad to come to your village"



# Use natural means to increase population. Long.
@ruleset.TaskType_Exp_Define
class Baby:
    textid = "baby"
    popsize = 2
    length = 3600
    shortdesc = "Use natural means to increase population"
    effectdesc = "Increases population by 1"
    reqs = { "building:townhall" : greater(1),
             "building:huts" : greater(1) }

    def collect_rewards(village):
        village.add_res('population', 1)
        return "Oooooh. Baby!"


# An expedition giving a small amount of food
@ruleset.TaskType_Exp_Define
class CollectNuts:
    textid = "collectnuts"
    popsize = 2
    length = 10
    shortdesc = "Send villagers to collect some nuts"
    effectdesc = "Increases food by 5"
    reqs = { "building:townhall" : greater(1) }

    def collect_rewards(village):
        village.add_res('food', 5)
        return "You found some nuts."
    

# An expedition giving a small amount of wood
@ruleset.TaskType_Exp_Define
class CutWood:
    textid = "cutwood"
    popsize = 4
    length = 30
    shortdesc = "Send some villagers to cut wood"
    effectdesc = "Increases wood by 5"
    reqs = { "building:townhall" : greater(1) }

    def collect_rewards(village):
        village.add_res('wood', 5)
        return "You found some wood."


# An expedition giving a large amount of food
@ruleset.TaskType_Exp_Define
class HuntAnimals:
    textid = "huntanimals"
    popsize = 5
    length = 90
    shortdesc = "Send hunters to catch some animals" 
    effectdesc = "Increases food by 50"
    reqs = { "building:townhall": greater(2),
             "building:farm": greater(1) }

    def collect_rewards(village):
        village.add_res('food', 50)
        return "You caught a deer."


# An expedition giving a large amount of wood
@ruleset.TaskType_Exp_Define
class FreeWood:
    textid = "freewood"
    popsize = 1
    length = 2
    shortdesc = "Get a free stack of wood"
    effectdesc = "Increases wood by 200"
    reqs = { "building:townhall" : greater(1) }

    def collect_rewards(village):
        village.add_res('wood', 200)
        return "The gods of testing grant you a stack of wood."


