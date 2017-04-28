from gamedata.common.keywords import *

from .ruleset import ruleset

# Improves farm production
@ruleset.TechType_Declare('irrigation')
class irrigation:
    building_src = 'farm'
    name = "Irrigation"
    shortdesc = "Improves food yield of farms"
    develop = { "cost" : { 'wood' : 100 },
                "pops" : 10,
                "time" : 7200,
                "reqs" : { 'building:farm' : greater(5) } }

irrigation.provides("property:farmefficiency", fixed('0.25'))

# Allows trading
@ruleset.TechType_Declare('currency')
class trading:
    building_src = 'townhall'
    name = 'Currency'
    shortdesc = "The creation of currency allows trade within the village and with strangers"
    develop = { "cost" : { },
                "pops" : 10,
                "time" : 7200,
                "reqs" : { 'building:townhall' : greater(1),
                           'total:population' : greater(10) } }
