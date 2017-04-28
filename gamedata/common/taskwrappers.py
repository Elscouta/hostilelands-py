from types import MethodType

from django.core.exceptions import ValidationError

from gamedata.common.utils import *
from gamedata.common.tasktypes import StaticTaskTemplate, TaskTemplate
from gamedata.common.keywords import *

# Represents any construction task.
# Must be initialized with the building name (which is
# trusted to be valid)
class TaskType_Construct_Building(StaticTaskTemplate):

    def __init__(self, ruleset, building_type):
        
        self.building_textid = building_type.get_textid()
        self.building_desc = building_type

        reqs = self.building_desc.construction["reqs"]
        reqs['building:'+self.building_textid] = exact(0)

        def generate_effectdesc(village):
            return stringify_property_effects(self.building_desc.get_property_effects(1, village))
        
        def collect_rewards(village):
            if (village.get_building_level(self.building_textid) > 0):
                return "This building was already built!"
            village.add_building(self.building_textid)
            
            return "A new building has been built!"
        
        StaticTaskTemplate.__init__(self,
            ruleset = ruleset,
            textid = "constructbuilding/" + self.building_textid,
            cost = self.building_desc.construction["cost"],
            uses = { "population" : self.building_desc.construction["pops"] },
            reqs = reqs,
            length = self.building_desc.construction["time"],
            shortdesc = "Build a " + self.building_desc.name,
            tags = [ 'project', 'townhall' ],
            unique = True,
            generate_effectdesc = generate_effectdesc,
            collect_rewards = collect_rewards
        )


# Represents the process of upgrading a building.
# Requires a parameter specifying the level to which you want 
# to upgrade. You can set the parameter either explicitly or
# through guess_param, but it must be set before calling any
# function.
class TaskType_Upgrade_Building(TaskTemplate):
    
    def __init__(self, ruleset, building_type):
        self.building_textid = building_type.get_textid()
        self.building_desc = building_type
    
        TaskTemplate.__init__(self, ruleset, "upgradebuilding/" + self.building_textid, { "level" })

    def params_for_village(self, village):
        return { "level" : village.get_building_level(self.building_textid) + 1 }

    def get_cost(self, level):
        return { k: v(level) for k, v in self.building_desc.upgrade["cost"].items() }

    def get_uses(self, level):
        return { "population" : self.building_desc.upgrade["pops"](level) }
    
    def get_reqs(self, level):
        if (level < 2):
            return { 'core:never': exact(1) }
        reqs = { k: v(level) for k, v in self.building_desc.upgrade["reqs"].items() }
        reqs['building:'+self.building_textid] = exact(level - 1)
        return reqs

    def is_unique(self):
        return True

    def get_length(self, level):
        return self.building_desc.upgrade["time"](level)

    def get_shortdesc(self, level):
        return "Upgrade our " + self.building_desc.name + " to level " + str(level)
    

    def get_tags(self):
        return [ 'project', self.building_textid ]

    def get_generate_effectdesc(self, level):
        def generate_effectdesc(village):
            effects1 = self.building_desc.get_property_effects(level-1, village)
            effects2 = self.building_desc.get_property_effects(level, village)

            return stringify_property_effects_diff(effects1, effects2)
        
        return generate_effectdesc

    def get_collect_rewards(self, level):
        def collect_rewards(village):
            if (village.get_building_level(self.building_textid) >= level):
                return "This building is already at this level. No upgrade performed."
            if (village.get_building_level(self.building_textid) < level - 1):
                return "This building isn't at a high enough level. No upgrade performed."
            
            village.set_building_level(self.building_textid, level)
            return "A building got upgraded!"
        
        return collect_rewards

# Represent the process of developing a new technology
# Does not require a parameter
class TaskType_Develop_Tech(StaticTaskTemplate):

    def __init__(self, ruleset, tech_type):
        self.tech_textid = tech_type.get_textid()
        self.tech_desc = tech_type
        
        reqs = self.tech_desc.develop["reqs"]
        reqs["tech:"+self.tech_textid] = exact(0)

        def collect_rewards(village):
            if (village.has_tech(self.tech_textid)):
                return "This technology was already developped!"
            village.add_tech(self.tech_textid)
            return "A new technology is available!"
        
        StaticTaskTemplate.__init__(self,
            ruleset = ruleset,
            textid = "developtech/" + self.tech_textid,
            cost = self.tech_desc.develop["cost"],
            uses = { "population" : self.tech_desc.develop["pops"] },
            reqs = reqs,
            length = self.tech_desc.develop["time"],
            unique = True,
            shortdesc = "Develop " + self.tech_desc.name,
            tags = [ 'project', self.tech_desc.building_src ],
            generate_effectdesc = lambda village: "",
            collect_rewards = collect_rewards
        )

