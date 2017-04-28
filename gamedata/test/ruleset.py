from gamedata.common.ruleset import Ruleset

ruleset = Ruleset()

def init_village(v):
    v.add_building("townhall")
    v.add_building("farm")

    v.add_res("population", 10)
    v.set_policy("hours_leisure", 6)
    v.set_policy("hours_work", 10)
    v.set_policy("food_allowance", 100)

ruleset.init_village = init_village

def get_ruleset():
    return ruleset
