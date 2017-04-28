from django.db import models

from game import models as village

##
# A building in a village. Inherits the properties from the associated
# BuildingType
# 
class Building(models.Model):
    hometown = models.ForeignKey(village.Village)
    textid = models.CharField("Identifier", max_length=30, default='Error')
    level = models.IntegerField("Level", default=0)

    def __str__(self):
        return self.get_buildingtype().name + " (Level " + str(self.level) + ")"

    def get_buildingtype(self):
        return self.hometown.get_ruleset().get_buildingtype(self.textid)

#    @expose_property("building:(?P<textid>[a-z]*)")
    def get_level(self):
        return self.level

    def get_template_view(self):
        return self.get_buildingtype().template_view

    def get_absolute_url(self):
        return reverse("game.building.show", { "village_id" : self.hometown.pk,
                                               "building_textid" : self.textid })

