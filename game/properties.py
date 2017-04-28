from game.exceptions import *

def validate_input(proptype, strvalue):
    if (not proptype.uc):
        raise ForbiddenError("Operation not permitted")
        
    ivalue = int(strvalue)
    if (ivalue < proptype.min_value):
        raise GameRulesViolation("Value too low")

    if (ivalue > proptype.max_value):
        raise GameRulesViolation("Value too high")

    return ivalue

