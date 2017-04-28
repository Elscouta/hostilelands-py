from gamedata.common.keywords import *
from .ruleset import ruleset

@ruleset.TaskType_Exp_Define
class AddWood:
    textid = "addwood"
    popsize = 1
    length = 10
    shortdesc = "test addwood"

    reqs = { "building:townhall" : greater(1) }

    def collect_rewards(village):
        village.add_res('wood', 1)
        return "+1 wood"

@ruleset.TaskType_Exp_Define
class UseFive:
    textid = "usefive"
    popsize = 5
    length = 10
    shortdesc = "test:five"

    reqs = { "building:townhall" : greater(1) }

    def collect_rewards(village):
        return ""


@ruleset.TaskType_Exp_Define
class Exp_Unique:
    textid = "unique"
    popsize = 0
    length = 10
    shortdesc = "test:unique"
    unique = True

    reqs = { "building:townhall" : greater(1) }

    def collect_rewards(village):
        return ""

@ruleset.TaskType_Exp_Define
class Exp_Impossible:
    textid = "impossible"
    popsize = 0
    length = 10
    shortdesc = "test:impossible"

    reqs = { "core:never" : greater(1) }

    def collect_rewards(village):
        return ""

