from django.contrib import admin

from .models import *
from .building import Building

admin.site.register(Village)
admin.site.register(Hero)
admin.site.register(Task)
admin.site.register(Building)
admin.site.register(Property)
admin.site.register(Ressource)
admin.site.register(CommitedRessource)
admin.site.register(Event)
