from gamedata.common.keywords import *

from .ruleset import ruleset

@ruleset.TaskType_Continuous_Define
class Farmer:
    textid = 'farmer'
    building_src = 'farm'
    reqs = { 'building:farm' : greater(3) }
    shortdesc = 'Help at the farm'
    effectdesc = 'By helping at the farm, a worker can improve the generation of food by a flat amount'

Farmer.while_running_by("workers").provides("production:food", linear("0.1"))
