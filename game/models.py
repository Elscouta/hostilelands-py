from decimal import Decimal
from datetime import timedelta
import json

from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.forms import ModelForm
from django.utils import timezone

from gamedata.common.utils import pack_task_params, unpack_task_params
from game.exceptions import *
from game import loader

##
# The main class in a game. Acts as a hub for everything happening.
#
class Village(models.Model):
    #####################################################################
    #                                                                   #
    #                           Database fields                         #
    #                                                                   #
    #####################################################################
    name = models.CharField('Name', max_length=30, default='Undefined')
    simulation_time = models.DateTimeField('Simulated Up To')
    
    #####################################################################
    #                                                                   #
    #                       DJANGO-RELATED MECANISMS                    #
    #                                                                   #
    #####################################################################
            
    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        return reverse("game.village", kwargs = { "village_id" : self.pk })

    #####################################################################
    #                                                                   #
    #                 GAME-RELATED MECANISMS : RESSOURCES               #
    #                                                                   #
    #####################################################################
    
    # Updates a ressource field. Calling this with an invalid ressource identifier
    # will cause (harmless) database pollution.
    # Applies ressource limit (0 and storage max)
    # 
    # Trying to remove commited ressources will silently fail.
    # FIXME: If storage becomes lower than amount of commited ressources, corruption will occur.
    # Does save to database.
    def add_res(self, res, delta):
        try:
            row = Ressource.objects.get(hometown=self, textid=res)
        except Ressource.DoesNotExist:
            row = Ressource(hometown=self, textid=res, total=0)
        val = row.total + Decimal(delta)

        limit = self.get_res_storage(res)
        if (val < row.occupied):
            val = row.occupied
        if (val > limit):
            val = limit

        row.total = val
        row.save()

    # Gets a ressource field. Returns 0 if called with an invalid ressource identifier
    def get_res_total(self, res):
        try:
            return Ressource.objects.get(hometown=self, textid=res).total
        except Ressource.DoesNotExist:
            return Decimal(0)
    
    # Gets a ressource field. Returns 0 if called with an invalid ressource identifier
    def get_res_free(self, res):
        try:
            return Ressource.objects.get(hometown=self, textid=res).get_free()
        except Ressource.DoesNotExist:
            return Decimal(0)

    # Returns the current production of the given ressource, based on the buildings in the
    # village. Must be a valid ressource
    def get_res_production(self, res):
        return self.get_property_value("production:"+res)

    # Returns the current storage of the given ressource, based on the buildings in the 
    # village. Returns 0 if res is not a valid ressource
    def get_res_storage(self, res):
        return self.get_property_value("storage:"+res)


    # Checks whether the village can pay the provided costs. 
    # Must be provided with a valid cost structure
    def has_available_res(self, costs):
        for k, v in costs.items():
            if (self.get_res_free(k) < v):
                return False

        return True


    # Pays costs and saves to database. No checking performed,
    # call has_available_res before if needed.
    def pay_res(self, costs):
        for k, v in costs.items():
            self.add_res(k, -v)

        self.save()

    # Commits ressources to a task. Minimal checking performed,
    # you should call has_available_res before if needed.
    def commit_res(self, uses, task):
        for k, v in uses.items():
            if (v == 0):
                continue
            
            r = Ressource.objects.get(hometown=self, textid=k)
            r.occupied += Decimal(v)
            r.save()
            r2 = CommitedRessource(task=task, ressource=r, quantity=Decimal(v))
            r2.save()

    # Frees ressources associated to a task.
    def free_res(self, task):
        res = CommitedRessource.objects.filter(task=task)
        for r in res:
            assert(r.ressource.occupied >= r.quantity)
            r.ressource.occupied -= r.quantity
            r.ressource.save()

        res.delete()
    
    #####################################################################
    #                                                                   #
    #                 GAME-RELATED MECANISMS : BUILDINGS                #
    #                                                                   #
    #####################################################################
    # Adds a building to the village. Does not take into account game logic.
    # The building should not be present already!
    # Saves to database
    def add_building(self, name):
        from game.building import Building
        
        building = Building()
        building.hometown = self
        building.textid = name
        building.level = 1
        building.save()

    # Sets the level of a building to a different value. Does not take into
    # account game logic. The building must be present already!
    # Saves to database
    def set_building_level(self, bname, blevel):
        from game.building import Building

        building = Building.objects.get(hometown=self.pk, textid=bname)
        building.level = blevel
        building.save()

    # Returns the level of the building in the village. 0, if it doesn't 
    # exist or is not a valid building name
    def get_building_level(self, bname):
        from game.building import Building

        try:
            building = Building.objects.get(hometown=self.pk, textid=bname)
            return building.level
        except (Building.DoesNotExist):
            return 0
        except (Building.MultipleObjectsReturned):
            raise UnexpectedState("Multiple buildings named {} in {}", bname, self)
            assert(0)
    
    #####################################################################
    #                                                                   #
    #                 GAME-RELATED MECANISMS : TECHS                    #
    #                                                                   #
    #####################################################################
    # Checks if the technology is present in the village
    def has_tech(self, tech_textid):
        try:
            p = Property.objects.get(hometown=self.pk, textid="tech:" + tech_textid)
            return p.value > 0
        except (Property.DoesNotExist):
            return False

    # Adds the technology to the village. Does nothing if the technology is
    # already present
    def add_tech(self, tech_textid):
        Property(hometown = self,
                 textid = "tech:" + tech_textid,
                 value = 1).save()



    #####################################################################
    #                                                                   #
    #                 GAME-RELATED MECANISMS : PROPERTIES               #
    #                                                                   #
    #####################################################################
    # Returns the value of a given property, which might be a building 
    # level, or whatever.
    def get_property_value(self, prop):
        arr = prop.split(':')
    
        if (arr[0] == 'building'):
            return self.get_building_level(arr[1])
        
        elif (arr[0] == 'total'):
            return self.get_res_total(arr[1])
        
        elif (arr[0] == 'core'):
            return Decimal(0)
        
        elif (arr[0] == 'policy'):
            try:
                p = Property.objects.get(hometown=self.pk, textid=prop)
                return p.value
            except (Property.DoesNotExist):
                raise Exception("Undefined policy: " + prop)
        
        elif (arr[0] == 'tech'):
            try:
                p = Property.objects.get(hometown=self.pk, textid=prop)
                return float(p.value)
            except (Property.DoesNotExist):
                return Decimal(0)

        elif (arr[0] == 'task'):
            base_textid = arr[1]
           
            tasks = Task.objects.filter(hometown = self, base_textid = base_textid)

            if (len(arr) == 2):
                return tasks.count()

            else:
                value = 0
                for task in tasks:
                    value += task.get_param(arr[2]) 

                return value
        
        else:
            return self.get_ruleset().get_propertytype(prop).get_value(self)

    
    # Sets a given property in the database. No checks are performed. This will
    # not fail, but have no effect if the property is not a policy
    def set_property_value(self, prop, v):
        try:
            p = Property.objects.get(hometown=self.pk, textid=prop)
            p.value = v
            p.save()
        except (Property.DoesNotExist):
            p = Property(hometown=self, textid=prop, value=v)
            p.save()

    # Wrapper around set_property_value. You should probably use this
    def set_policy(self, name, v):
        self.set_property_value("policy:"+name, v)


    # Checks if all requirements are fulfilled
    # reqs must be a dictionnary enumerating requirements. A
    # requirement associates to a property value a function
    # returning whether this property value is valid
    def has_reqs(self, reqs):
        for k, v in reqs.items():
            if not v(self.get_property_value(k)):
                return False

        return True

    #####################################################################
    #                                                                   #
    #                   GAME-RELATED MECANISMS : TASKS                  #
    #                                                                   #
    #####################################################################
    # Checks whether a task with this base identifier exists in the
    # town
    def has_task(self, base_textid):
        return Task.objects.filter(hometown=self.pk,base_textid=base_textid).count() > 0

    # Returns the task matching the given base textid.
    def get_task(self, base_textid):
        return Task.objects.get(hometown=self.pk, base_textid=base_textid)

    #####################################################################
    #                                                                   #
    #                 GAME-RELATED MECANISMS : RULESET                  #
    #                                                                   #
    #####################################################################
    # Returns the ruleset used for the village
    def get_ruleset(self):
        return loader.get_ruleset()

##
# Used to instantiate a new village (by a user)
#
class VillageForm(ModelForm):
    class Meta:
        model = Village
        fields = [ 'name' ]

    def save(self):
        v = super(VillageForm, self).save(commit=False)
        v.simulation_time = timezone.now()
        v.save()
        
        v.get_ruleset().init_village(v)

        return v

class Task(models.Model):
    hometown = models.ForeignKey(Village)
    base_textid = models.CharField('Type', max_length=80, default='Error')
    params = models.CharField('Params', max_length=80, default='')
    start_time = models.DateTimeField('Start Time')
    completion = models.DecimalField('Completion', max_digits=16, decimal_places=3, default=0) 
    length = models.IntegerField('Required Time', default=0)

    def __str__(self):
        if (self.is_continuous()):
            return self.get_textid() + " -- started on {}".format(self.start_time)
        else:
            return self.get_textid() + " -- started on {}, completion: {}/{}".format( 
                                  self.start_time, 
                                  self.completion,
                                  self.length)

    @classmethod
    def create(cls, village, tasktype):
        t = cls(hometown=village, 
                base_textid=tasktype.get_base_textid(),
                params=pack_task_params(tasktype.get_params()),
                start_time=timezone.now(),
                completion=0,
                length=tasktype.get_length())
        t.save()
        return t

    def get_textid(self):
        if (self.params == ''):
            return self.base_textid
        else:
            return self.base_textid + "[" + self.params + "]"

    def get_param(self, paramid):
        return unpack_task_params(self.params)[paramid]

    def set_params(self, params):
        self.params = pack_task_params(params)
        self.save()

    def is_finished(self):
        return self.completion >= self.length

    def is_continuous(self):
        return self.length == 0

    def get_current_completion(self):
        if (self.completion > self.length):
          return self.length
        else:
          return int(self.completion)

class Hero(models.Model):
    hometown = models.ForeignKey(Village)
    name = models.CharField('Name', max_length=30, default='Undefined')
    level = models.IntegerField('Level', default=1)
    def __str__(self):
        return self.name

class Property(models.Model):
    hometown = models.ForeignKey(Village)
    textid = models.CharField('Identifier', max_length=80, default='Undefined')
    value = models.DecimalField('Value', max_digits=16, decimal_places=3, default=1)
    def __str__(self):
        return self.textid + " = " + str(self.value)

class Ressource(models.Model):
    hometown = models.ForeignKey(Village)
    textid = models.CharField('Ressource Identifier', max_length=30, default='Undefined')
    total = models.DecimalField('Total', max_digits=16, decimal_places=3, default=0)
    occupied = models.DecimalField('Occupied', max_digits=16, decimal_places=3, default=0)

    def get_free(self):
        return self.total - self.occupied

    def __str__(self):
        return self.textid + " : " + str(self.total) + " (" + str(self.occupied) + " used) in " + self.hometown.name

class CommitedRessource(models.Model):
    ressource = models.ForeignKey(Ressource)
    task = models.ForeignKey(Task)
    quantity = models.DecimalField('Amount', max_digits=16, decimal_places=3, default=0)

    def __str__(self):
        return str(self.quantity) + " " + self.ressource.textid + " used on " + self.task.get_textid()

class Event(models.Model):
    hometown = models.ForeignKey(Village)
    textid = models.CharField('Event Identifier', max_length=30, default='Undefined')
    context = models.TextField('Context', max_length=500, default='{}')
    time = models.DateTimeField('Time of event')
    unread = models.BooleanField('Is Unread', default=True)

    @classmethod
    def create(cls, hometown, eventtype, context, time):
        e = cls(hometown = hometown,
                textid = eventtype.get_textid(),
                context = json.dumps(context),
                time = time,
                unread = True)
        e.save()

        return e

    def get_absolute_url(self):
        return reverse('event:get', village_id=hometown, event_id=self.pk)

    def get_context(self):
        return json.loads(self.context)

    def mark_read(self):
        self.unread = False
        self.save()

    def __str__(self):
        return "{} with context: {}".format(self.textid, self.context)
