from gamedata.common.keywords import *

from .ruleset import ruleset

@ruleset.TaskType_Continuous_Define
class Farmer:
    textid = 'farmer'
    building_src = 'farm'
    reqs = { 'building:farm' : greater(3) }
    shortdesc = 'Recruit a farmer'
    effectdesc = 'By helping at the farm, a worker can improve the generation of food by a flat amount'

Farmer.while_running_by("workers").provides("production:food", linear("0.05"))

@ruleset.TaskType_Continuous_Define
class Woodcutter:
    textid = 'woodcutter'
    building_src = 'sawmill'
    reqs = { 'building:sawmill' : greater(1) }
    shortdesc = 'Recruit a woodcutter'
    effectdesc = 'A woodcutter will ensure additionnal wood production'

Woodcutter.while_running_by("workers").provides("production:wood", linear("0.05"))

@ruleset.TaskType_Continuous_Define
class Carpenter:
    textid = 'carpenter'
    building_src = 'carpenter'
    reqs = { 'building:sawmill' : greater(3) }
    shortdesc = 'Recruit a carpenter'
    effectdesc = 'A carpenter will improve the efficiency of sawmills'

Carpenter.while_running_by("workers").provides("property:sawmillefficiency", linear("0.05"))
