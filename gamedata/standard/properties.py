from gamedata.common.keywords import fixed,linear,add,multiply

from .ruleset import ruleset

# POLICIES
p = ruleset.PropertyType_Declare("policy:hours_work")
p.user_choice(0, 12)

p = ruleset.PropertyType_Declare("policy:hours_leisure")
p.user_choice(0, 12)

p = ruleset.PropertyType_Declare("property:hours_rest", '24')
p.modified_by("policy:hours_work", add('-1'))
p.modified_by("policy:hours_leisure", add('-1'))

p = ruleset.PropertyType_Declare("property:foodconsumption", 1)
p.consumes("food", linear('0.1')).modified_by("total:population", multiply())

# PROPERTY
p = ruleset.PropertyType_Declare("property:work_multiplier", '0')
p.modified_by("policy:hours_work", add('0.1'))

# TECHS
p = ruleset.PropertyType_Declare("property:farmefficiency", 1)
p = ruleset.PropertyType_Declare("property:sawmillefficiency", 1)
