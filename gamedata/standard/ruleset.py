from gamedata.common.ruleset import Ruleset

ruleset = Ruleset()

def init_village(v):
    v.add_building("townhall")
    v.add_building("farm")

    v.add_res("population", 10)
    v.add_res("food", 25)

    v.set_policy("hours_leisure", 6)
    v.set_policy("hours_work", 10)

ruleset.init_village = init_village

def get_ruleset():
    return ruleset

