class ForbiddenError(Exception):
    def __init__(self, msg, *args):
        self.msg = msg.format(*args)

    def __str__(self):
        return "ForbiddenError: " + self.msg

class GameRulesViolation(Exception):
    def __init__(self, msg, *args):
        self.msg = msg.format(*args)

    def __str__(self):
        return "GameRulesViolation: " + self.msg

class InsufficientRessourcesViolation(GameRulesViolation):
    def __init__(self, msg, village, costs = {}, uses = {}):
        self.msg = msg
        self.village = village
        self.costs = costs
        self.uses = uses

    def __str__(self):
        msg = "InsufficientRessourcesViolation: " + self.msg
        if (self.costs):
            msg += "Cost: " + str(self.costs)
        if (self.uses):
            msg += "Uses: " + str(self.uses)
        return msg

class InvalidIdentifier(Exception):
    def __init__(self, msg, *args):
        self.msg = msg.format(*args)

    def __str__(self):
        return "InvalidIdentifier: " + self.msg

class InvalidPropertyName(InvalidIdentifier):
    def __init__(self, ruleset, property_textid):
        self.property_textid = property_textid
        self.ruleset = ruleset

    def __str__(self):
        msg = "InvalidPropertyName: Unknown identifier: " + str(self.property_textid) + "\n"
        msg += "Registered property text identifiers are: \n"

        try:
            for prop_textid in self.ruleset.get_all_propertytypes().keys():
                msg += " * " + str(prop_textid) + "\n"
        except:
            msg += " (failed to dump ruleset: {})".format(self.ruleset)

        return msg

class InvalidBuildingName(InvalidIdentifier):
    def __init__(self, building_textid):
        self.building_textid = building_textid

    def __str__(self):
        msg = "InvalidBuildingName: Unknown identifier: " + self.building_textid + "\n"
        msg += "Registered building text identifiers are: \n"

        for building_textid in loader.get_all_buildingtypes().keys():
            msg += " * " + prop_textid

        return msg

class InvalidTaskName(InvalidIdentifier):
    def __init__(self, task_textid):
        self.task_textid = task_textid

    def __str__(self):
        msg = "InvalidTaskName: Unknown identifier: " + self.task_textid + "\n"
        msg += "Registered task templates identifiers are: \n"

        for task_textid in loader.get_all_tasktemplates().keys():
            msg += " * " + task_textid

        return msg

class InvalidEventName(InvalidIdentifier):
    def __init__(self, ruleset, event_textid):
        self.ruleset = ruleset
        self.event_textid = event_textid
    
    
    def __str__(self):
        msg = "InvalidPropertyName: Unknown identifier: " + str(self.event_textid) + "\n"
        msg += "Registered event text identifiers are: \n"

        try:
            for event_textid in self.ruleset.get_all_eventtypes().keys():
                msg += " * " + str(event_textid) + "\n"
        except:
            msg += " (failed to dump ruleset: {})".format(self.ruleset)

        return msg

class InternalServerError(Exception):
    def __init__(self, msg, *args):
        self.msg = msg.format(*args)

    def __str__(self):
        return "InternalServerError: " + self.msg

class UnexpectedState(Exception):
    def __init__(self, msg, *args):
        self.msg = msg.format(*args)

    def __str__(self):
        return "UnexpectedState: " + self.msg
