from decimal import Decimal
from types import MethodType


from gamedata.common.keywords import add,add_transf,multiply


# 
class PropertyType(object):
    def __init__(self, ruleset, name, bv = 0):
        global property_types
        
        self.ruleset = ruleset
        self.textid = name
        self.base_value = Decimal(bv)
        # This is what is authoritative regarding the relations between 
        # properties
        self.modifications = [] 
        # This is a reverse cache of applied modifications, that were registered
        # through .provides and .consumes. It is not guaranteed to be complete, as
        # other effects can be directly registered by .modified_by.
        self.internal_provides = []
        self.internal_consumes = []

        self.uc = False
        self.min_value = 0
        self.max_value = 0

    def modified_by(self, dep_textid, rule):
        self.modifications.append({ "property_textid" : dep_textid, "rule" : rule })

    # CAREFUL: The same property cannot be both provided and consumed
    def consumes(self, ressource_textid, transf):
        p = self.ruleset.PropertyType_Declare("internal[" + self.textid + "]:" + "consume:" + ressource_textid)
        p.modified_by(self.textid, add_transf(transf))

        self.ruleset.get_propertytype("production:" + ressource_textid).modified_by(p.textid, add(-1))

        self.internal_consumes.append({ "textid" : "production:" + ressource_textid,
                                        "prop"   : p, 
                                        "transf" : transf})
        return p

    # CAREFUL: The same property cannot be both provided and consumed
    def provides(self, property_textid, transf):
        p = self.ruleset.PropertyType_Declare("internal[" + self.textid + "]:" + property_textid)
        p.modified_by(self.textid, add_transf(transf))

        self.ruleset.get_propertytype(property_textid).modified_by(p.textid, add(1))

        self.internal_provides.append({ "textid" : property_textid,
                                        "prop"   : p, 
                                        "transf" : transf})
        return p
        
    
    def get_value(self, village):
        value = self.base_value

        for modif in self.modifications:
             modifier_value = village.get_property_value(modif['property_textid'])
             value = modif['rule'](value, modifier_value)

        return value

    def get_hypothetical_value(self, village, hyps):
        value = self.base_value

        for modif in self.modifications:
            if (modif['property_textid'] in hyps):
                modifier_value = hyps[modif['property_textid']]
            else:
                modifier_value = village.get_property_value(modif['property_textid'])
            value = modif['rule'](value, modifier_value)

        return value

    def user_choice(self, minv, maxv):
        self.uc = True
        self.min_value = minv
        self.max_value = maxv

    # Returns a property effects list of the form:
    # { propid_1 (string) => { "base" => (decimal), "actual" => (decimal) }
    #   propid_2 (string) => { "base" => (decimal), "actual" => (decimal) }
    #   ...
    # }
    # 
    # base gives the amount that would be given by the property if no
    # other property would be altering it.
    #
    # actual gives the amount that is given, taking all other properties
    # into account.
    #
    # Please note that this only returns effects declared through
    # .provides and .consumes, that are guaranteed to only add/substract
    # values to other properties.
    def get_property_effects(self, value, village):
        effects = {}
        
        for prov in self.internal_provides:
            effects[prov["textid"]] = { "base" : prov["transf"](value), 
                                        "actual" : prov["prop"].get_hypothetical_value(village, { self.textid : value }) }
            assert(type(effects[prov["textid"]]["base"]) in [Decimal, int])    # must be int or decimal
            assert(type(effects[prov["textid"]]["actual"]) in [Decimal, int])

        for cons in self.internal_consumes:
            assert(not prov.prop.textid in effects.keys())
            effects[cons["textid"]] = { "base" : -cons["transf"](value), 
                                        "actual" : -cons["prop"].get_hypothetical_value(village, { self.textid : value }) }
            assert(type(effects[cons["textid"]]["base"]) in [Decimal, int])    # must be int or decimal
            assert(type(effects[cons["textid"]]["actual"]) in [Decimal, int])

        return effects


##
# A type of building. Should be declared through the ruleset BuildingType_Declare
# instruction.
#
class BuildingType(object):
    def __init__(self, ruleset, textid, name, construction, upgrade):
        self.level_property = ruleset.PropertyType_Declare('building:' + textid, 0)

        self.textid = textid
        self.name = name
        self.template_view = "game/building/" + textid + ".html"
        self.construction = construction
        self.upgrade = upgrade

    def get_textid(self):
        return self.textid

    def consumes(self, ressource_textid, transf):
        return self.level_property.consumes(ressource_textid, transf)

    def provides(self, ressource_textid, transf):
        return self.level_property.provides(ressource_textid, transf)

    def get_property_effects(self, *args, **kwargs):
        return self.level_property.get_property_effects(*args, **kwargs)


class RessourceType(object):
    def __init__(self, textid, shortdesc, tags=[], category="misc"):
        self.textid = textid
        self.shortdesc = shortdesc
        self.tags = tags
        self.category = category
        self.on_negative = None

    def has_tag(self, tag):
        return tag in self.tags

    def get_textid(self):
        return self.textid

    def get_category(self):
        return self.category


class TechType(object):
    def __init__(self, ruleset, textid, building_src, name, shortdesc, develop):
        self.tech_property = ruleset.PropertyType_Declare('tech:' + textid, 0)

        self.textid = textid
        self.building_src = building_src
        self.name = name
        self.shortdesc = shortdesc
        self.develop = develop

    def get_textid(self):
        return self.textid
    
    def consumes(self, ressource_textid, transf):
        return self.tech_property.consumes(ressource_textid, transf)

    def provides(self, ressource_textid, transf):
        return self.tech_property.provides(ressource_textid, transf)

class EventType(object):
    def __init__(self, textid, template_name, handler):
        self.textid = textid
        self.template = "gamedata/events/" + template_name
        self.handler = handler

    def __call__(self, village):
        return self.handler(village)

    def get_textid(self):
        return self.textid
        
