import regex
from decimal import Decimal

from django.template.loader import get_template
from django.template import Context

# Merges two costs structure
def merge_costs(cost1, cost2):
    c = {}

    for k,v in cost1.items():
        c[k] = v

    for k,v in cost2.items():
        if (k in c.keys()):
            c[k] += v
        else:
            c[k] = v

    return c

# Returns a user-readable description of effects. Parameter must be of 
# the format returned by get_property_effects
def stringify_property_effects(effects):
    t = get_template("gamedata/effects_simple.html")
    c = Context({ "effects": effects })
    
    return t.render(c)

def stringify_property_effects_diff(effects1, effects2):
    for prop_textid, eff in effects1.items():
        if (not prop_textid in effects2.keys()):
            effects2[prop_textid] = { "base" : 0, "actual" : 0 }
    
    for prop_textid, eff in effects2.items():
        if (not prop_textid in effects1.keys()):
            effects1[prop_textid] = { "base" : 0, "actual" : 0 }

    effects = {}
    for prop_textid in effects1.keys():
        effects[prop_textid] = { "base1"   : effects1[prop_textid]["base"],
                                 "actual1" : effects1[prop_textid]["actual"],
                                 "base2"   : effects2[prop_textid]["base"],
                                 "actual2" : effects2[prop_textid]["actual"] }
    
    t = get_template("gamedata/effects_diff.html")
    c = Context({ "effects": effects })
    
    return t.render(c)
                       
# Turns a hashtable of task parameters into a string
def pack_task_params(params):
    packed = ""

    for key,val in params.items():
        packed += key
        packed += "="
        packed += str(val)
        packed += ","

    return packed

# Performs the reverse operation
def unpack_task_params(paramstr):
    match = regex.match(r"^(?:([a-z]+)=([0-9]+),?)*$", paramstr)
    
    if (match):
        params = {}

        for i in range(0, len(match.captures(1))):
            params[match.captures(1)[i]] = int(match.captures(2)[i])

        return params

    else:
        raise Exception("Invalid parameter string")

# Packs stuff
def pack_task_textid(base_textid, params):
    full_textid = base_textid 
    
    if (len(params.items()) > 0):
        full_textid += "["
        full_textid += pack_task_params(params)
        full_textid += "]"

    return full_textid


