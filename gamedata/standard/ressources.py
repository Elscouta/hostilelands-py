from .ruleset import ruleset

r = ruleset.RessourceType_Declare("population", "Citizens", tags=["integer", "noprod"], category="core")

r = ruleset.RessourceType_Declare("food", "Food", tags=["nouse"], category="basic")
r.on_negative = "starvation"

r = ruleset.RessourceType_Declare("wood", "Wood", tags=["nouse"], category="basic")
