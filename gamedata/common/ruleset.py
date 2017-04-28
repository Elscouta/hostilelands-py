import regex

from gamedata.common.datatypes import BuildingType, PropertyType, RessourceType, EventType, TechType
from gamedata.common.tasktypes import TaskType_Exp, TaskType_Continuous
from gamedata.common.taskwrappers import TaskType_Construct_Building, TaskType_Upgrade_Building, TaskType_Develop_Tech
from gamedata.common.utils import unpack_task_params

from game.exceptions import *

class Ruleset(object):
    def __init__(self):
        self.task_templates = {}
        self.property_types = {}
        self.building_types = {}
        self.ressource_types = {}
        self.tech_types = {}
        self.event_types = {}

    #################################################################
    #                                                               #
    #                    RULESET DECLARATION                        # 
    #                                                               #
    #################################################################
   
    def _create_object_from_skeleton(self, cls, inst, **extras):
        userattrs = { k:v for k,v in inst.__dict__.items() if not k.startswith('_') }

        for k,v in extras.items():
            userattrs[k] = v

        o = cls(**userattrs)

        return o

    ##
    # Decorator to use to declare easily events
    # 
    def EventType_Declare(self, textid, template_name):
        def create_event(handler):
            e = EventType(textid, template_name, handler)
            self.event_types[textid] = e
            return e

        return create_event

    def TechType_Declare(self, textid):
        def create_tech(cls):
            tech = self._create_object_from_skeleton(TechType, cls, ruleset=self, textid=textid)
            self.tech_types[textid] = tech
            
            t = TaskType_Develop_Tech(self, tech)
            self.task_templates[t.get_textid()] = t

            return tech
        
        return create_tech

    def RessourceType_Declare(self, textid, shortdesc, tags=[], category="misc"):
        e = RessourceType(textid, shortdesc, tags, category)
        self.ressource_types[textid] = e

        self.PropertyType_Declare("storage:"+textid)
        self.PropertyType_Declare("production:"+textid)

        return e

    ##
    # Decorator to easily create buildings
    #
    def BuildingType_Declare(self, textid):
        def create_building(cls):
            b = self._create_object_from_skeleton(BuildingType, cls, ruleset=self, textid=textid)
            self.building_types[textid] = b
            
            t = TaskType_Construct_Building(self, b)
            self.task_templates[t.get_textid()] = t
            
            t = TaskType_Upgrade_Building(self, b)
            self.task_templates[t.get_textid()] = t

            return b
        
        return create_building

    def PropertyType_Declare(self, textid, bv=0):
        e = PropertyType(self, textid, bv)
        self.property_types[textid] = e
        return e

    ##
    # Decorator to use for the definition of expeditions
    #
    def TaskType_Exp_Define(self, cls):
        t = self._create_object_from_skeleton(TaskType_Exp, cls, ruleset=self)
        self.task_templates[t.get_textid()] = t
        return t

    ##
    # Decorator to use for the definition of continuous tasks
    # 
    def TaskType_Continuous_Define(self, cls):
        t = self._create_object_from_skeleton(TaskType_Continuous, cls, ruleset=self)
        self.task_templates[t.get_textid()] = t
        return t

    ##
    # Needs to be implemented to provide an initial shell for the
    # village
    # 
    @staticmethod
    def init_village(village):
        raise Exception("ruleset.init_village must be implemented")


    #################################################################
    #                                                               #
    #                        RULESET QUERIES                        # 
    #                                                               #
    #################################################################
    def get_tasktype(self, textid):
        return self.get_tasktype_altered(textid, {})

    def get_tasktype_altered(self, textid, custom_params):
        match = regex.match(r"^([a-z_]+/[a-z_]+)\[(.*)\]$", textid)
        if (match):
            params = unpack_task_params(match.group(2))
            for k, v in custom_params.items():
                params[k] = v

            return self.task_templates[match.group(1)](**params)
        else:
            return self.task_templates[textid](**custom_params)

    def get_all_tasktemplates(self):
        return self.task_templates

    def get_buildingtype(self, textid):
        return self.building_types[textid]

    def get_all_buildingtypes(self):
        return self.building_types

    def get_techtype(self, textid):
        return self.tech_types[textid]

    def get_all_techtypes(self):
        return self.tech_types

    def get_propertytype(self, textid):
        if (not textid in self.property_types):
            raise InvalidPropertyName(self, textid)

        return self.property_types[textid]

    def get_all_propertytypes(self):
        return self.property_types

    def get_ressourcetype(self, textid):
        return self.ressource_types[textid]

    def get_all_ressourcetypes(self):
        return self.ressource_types

    def get_eventtype(self, textid):
        if (not textid in self.event_types):
            raise InvalidEventName(self, textid)

        return self.event_types[textid]

    def get_all_eventtypes(self):
        return self.event_types

