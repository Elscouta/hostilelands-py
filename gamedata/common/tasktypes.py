from decimal import Decimal
from types import MethodType

from gamedata.common.keywords import add,add_transf,multiply
from gamedata.common.utils import pack_task_textid


#
# A TaskType is a purely immutable structure, generally
# generated through a template, or defined through
# inheritance of StaticTaskTemplate
#
class TaskType(object):
    
    def __init__(self,
                 textid, 
                 template,
                 params,
                 cost,
                 uses,
                 reqs,
                 length,
                 unique,
                 shortdesc,
                 tags,
                 generate_effectdesc,
                 collect_rewards):

        self.textid = textid
        self.template = template
        self.params = params
        self.cost = cost
        self.uses = uses
        self.reqs = reqs
        self.length = length
        self.unique = unique
        self.shortdesc = shortdesc
        self.tags = tags
        self.generate_effectdesc = generate_effectdesc
        self.collect_rewards = collect_rewards
    
    #####
    # TASKTYPE INTERFACE
    ##
    def get_textid(self):
        return self.textid

    def get_base_textid(self):
        return self.get_template().get_textid()

    def get_template(self):
        return self.template

    def get_params(self):
        return self.params

    def get_cost(self):
        return self.cost

    def get_uses(self):
        return self.uses
    
    def get_reqs(self):
        return self.reqs
    
    def get_length(self):
        return self.length
    
    def is_unique(self):
        return self.unique

    def get_shortdesc(self):
        return self.shortdesc

    def get_generate_effectdesc(self):
        return self.generate_effectdesc

    def get_tags(self):
        return self.tags

    def get_collect_rewards(self):
        return self.collect_rewards

    
    #####
    # HELPER FUNCTIONS
    ##
    def has_tag(self, name):
        return name in self.tags

    def has_all_tags(self, namelist):
        for name in namelist:
            if (not self.has_tag(name)):
                return False
        return True
    
    def get_longdesc(self, village):
        uses = self.get_uses()
        if ("population" in uses.keys()):
            pop = uses["population"]
        else:
            pop = 0
        return (self.get_shortdesc() + "<br />" + 
                "-- <br />" + 
                "Time required: " + str(self.get_length()) + "<br />" + 
                "Workers required: " + str(pop) + "<br />" + 
                "-- <br />" +
                self.get_generate_effectdesc()(village));

    def get_param(self, paramid):
        return self.get_params()[paramid]




# 
# A template for task types. Calling an object with a set of parameters
# will return a task type.
#
# Direct subclasses of TaskTemplate can either define attribute fields
# for static properties, or custom functions taking parameters.
#
class TaskTemplate(object):
    
    ####
    # TEMPLATE FUNCTIONS
    ##
    
    # Constructor. Base textid (without parameter).
    def __init__(self, ruleset, textid, param_ids):
        self.textid = textid

        self.runningtask_property = ruleset.PropertyType_Declare("task:" + textid, 0)
        self.paramtask_properties = { 
            paramid: ruleset.PropertyType_Declare("task:" + textid + ":" + paramid)
            for paramid in param_ids
        }

    # Returns a tasktype with the provided parameter
    def __call__(self, **params):
        return TaskType(textid = self.get_full_textid(**params),
                        template = self,
                        params = params,
                        cost = self.get_cost(**params),
                        uses = self.get_uses(**params),
                        reqs = self.get_reqs(**params),
                        length = self.get_length(**params),
                        unique = self.is_unique(),
                        shortdesc = self.get_shortdesc(**params),
                        tags = self.get_tags(),
                        generate_effectdesc = self.get_generate_effectdesc(**params),
                        collect_rewards = self.get_collect_rewards(**params))

    # Returns the textid, with the parameters enclosed in braces.
    def get_full_textid(self, **params):
        return pack_task_textid(self.textid, params)

    # Returns a set of possible parameters for the given village
    def params_for_village(self, village):
        return {}

    # Returns a tasktype suitable for the village. Not guaranteed to
    # fulfill all requirements.
    def for_village(self, village):
        return self(**self.params_for_village(village))

    # Exposes the runningtask property
    def while_running(self):
        return self.runningtask_property

    # Exposes a parameter property
    def while_running_by(self, param):
        return self.paramtask_properties[param]

    ####
    # DEFAULT, PARAMETER LESS, TASKTYPE DEFINITION 
    ##
    
    def get_textid(self, **params):
        return self.textid

    def get_cost(self, **params):
        return self.cost

    def get_uses(self, **params):
        return self.uses
    
    def get_reqs(self, **params):
        return self.reqs
    
    def get_length(self, **params):
        return self.length
    
    def is_unique(self):
        return self.unique

    def get_shortdesc(self, **params):
        return self.shortdesc

    def get_tags(self, **params):
        return self.tags

    def get_generate_effectdesc(self, **params):
        return self.generate_effectdesc

    def get_collect_rewards(self, **params):
        return self.collect_rewards




#
# A wrapper around TaskType that makes the class behave like a proper template.
#
class StaticTaskTemplate(TaskType, TaskTemplate):
    
    # Transfers everything to the TaskType, then performs 
    # template-related initialization.
    def __init__(self, ruleset, textid, **kwargs):
        TaskType.__init__(self, textid, self, {}, **kwargs)
        TaskTemplate.__init__(self, ruleset, textid, {})

    # Returns itself, as it fulfills both interfaces.
    def __call__(self):
        return self





#
# Describes an expedition, a (short), one-time task with custom rewards.
# Defining task type
#
class TaskType_Exp(StaticTaskTemplate):
    def __init__(self, ruleset, textid, shortdesc, popsize, length, reqs, collect_rewards, 
                 effectdesc="", unique=False):
        
        StaticTaskTemplate.__init__(self, 
            ruleset = ruleset,
            textid = "expedition/" + textid,
            cost = {},
            uses = { "population" : popsize },
            reqs = reqs,
            length = length,
            shortdesc = shortdesc,
            generate_effectdesc = lambda village: effectdesc,
            tags = [ "expedition" ],
            unique = unique,
            collect_rewards = collect_rewards
        )


#
# Describes a task that isn't limited in time, but provides constant benefits.
# 
class TaskType_Continuous(TaskTemplate):
    def __init__(self, ruleset, textid, building_src, shortdesc, reqs, effectdesc=""):
        TaskTemplate.__init__(self, ruleset, "job/" + textid, { "workers" })
        
        self.cost = {}
        self.reqs = reqs
        self.length = 0
        self.shortdesc = shortdesc
        self.generate_effectdesc = lambda village: effectdesc
        self.tags = [ "job", building_src ]
        self.unique = True
        self.collect_rewards = lambda village: None

    def params_for_village(self, village):
        return { "workers" : 1 }
    
    def get_uses(self, workers):
        return { "population" : workers }
        
    def get_shortdesc(self, workers):
        if (workers > 1):
            return self.shortdesc + " (" + str(workers) + ")"
        else:
            return self.shortdesc
