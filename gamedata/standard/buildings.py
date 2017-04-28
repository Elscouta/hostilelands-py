from gamedata.common.keywords import *

from .ruleset import ruleset
from . import properties, ressources

# TOWNHALL
@ruleset.BuildingType_Declare('townhall')
class townhall:
    name = "Town Hall"
    construction = { "cost" : { },
                     "pops" : 0,
                     "time" : 0,
                     "reqs" : { "core:never" : exact(1) } }

    upgrade =      { "cost" : { "wood" : linear(200) },
                     "pops" : linear(10),
                     "time" : linear(120),
                     "reqs" : { } }

townhall.provides("storage:wood", fixed(100))
townhall.provides("storage:food", fixed(500))
townhall.provides("storage:population", fixed(10))


# HUTS
@ruleset.BuildingType_Declare('huts')
class huts:
    name = 'Huts'
    construction = { "cost" : { "wood" : 50 },
                     "pops" : 5,
                     "time" : 180,
                     "reqs" : { "building:townhall" : greater(1) } }
    upgrade =      { "cost" : { "wood" : linear(50) },
                     "pops" : fixed(5),
                     "time" : linear(180),
                     "reqs" : { } }

huts.provides("storage:population", linear(5))


# FARM
@ruleset.BuildingType_Declare('farm')
class farm:
    name = 'Farm'
    construction = { "cost" : { "wood" : 25,
                              "food" : 25 },
                     "pops" : 5,
                     "time" : 180,
                     "reqs" : { "building:townhall" : greater(1) } }
    upgrade =      { "cost" : { "wood" : linear(25),
                                "food" : linear(25) },
                     "pops" : fixed(5),
                     "time" : linear(180),
                     "reqs" : { } }

farm.provides("storage:food", linear(50))
farm.provides("production:food", linear('0.1')).modified_by("property:farmefficiency", multiply())


# STOREHOUSE
@ruleset.BuildingType_Declare('storehouse')
class storehouse:
    name = 'Storehouse'
    construction = { "cost" : { "wood" : 50 },
                     "pops" : 10,
                     "time" : 240,
                     "reqs" : { "building:townhall" : greater(1) } }
    upgrade =      { "cost" : { "wood" : linear(50) },
                     "pops" : fixed(10),
                     "time" : linear(240),
                     "reqs" : { } }
storehouse.provides("storage:food", linear(250))
storehouse.provides("storage:wood", linear(200))


# SAWMILL
@ruleset.BuildingType_Declare('sawmill')
class sawmill:
    name = 'Sawmill'
    construction = { "cost" : { "wood" : 200 },
                     "pops" : 15,
                     "time" : 300,
                     "reqs" : { "building:townhall" : greater(1) } }
    upgrade =      { "cost" : { "wood" : linear(150) },
                     "pops" : fixed(15),
                     "time" : linear(240),
                     "reqs" : { } }
sawmill.provides("production:wood", linear(0.1))
sawmill.provides("storage:wood", linear(100))


