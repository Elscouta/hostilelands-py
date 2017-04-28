from gamedata.common.keywords import *
from .ruleset import ruleset

# POLICIES
p = ruleset.PropertyType_Declare("policy:hours_work")
p.user_choice(0, 12)

p = ruleset.PropertyType_Declare("policy:hours_leisure")
p.user_choice(0, 12)

p = ruleset.PropertyType_Declare("property:hours_rest", '24')
p.modified_by("policy:hours_work", add('-1'))
p.modified_by("policy:hours_leisure", add('-1'))

p = ruleset.PropertyType_Declare("policy:food_allowance")
p.user_choice(0, 100)
p.consumes("food", linear('0.001')).modified_by("total:population", multiply())


# PROPERTIES
p = ruleset.PropertyType_Declare("property:exhaustion", '60')
p.modified_by("property:hours_rest", add('-5'))
p.modified_by("policy:hours_leisure", add('-1'))
p.modified_by("policy:food_allowance", add('-0.1'))

p = ruleset.PropertyType_Declare("property:happyness", '0')
p.modified_by("policy:hours_leisure", add('5'))

p = ruleset.PropertyType_Declare("property:work_multiplier", '0')
p.modified_by("policy:hours_work", add('0.1'))

# TECHS
p = ruleset.PropertyType_Declare("property:farmefficiency", '1')
