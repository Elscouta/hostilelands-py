from django.test import TestCase
from django.utils import timezone

from datetime import timedelta
from decimal import Decimal

from gamedata.common import keywords as kwd
from game import models, loader, tasks, villages, testutils

class ModelTests(TestCase):
    def setUp(self):
        loader.load_gamedata("gamedata.test")

        self.village = villages.create_village("test")
        self.village.set_policy("food_allowance", 0)
        
        self.ruleset = self.village.get_ruleset()

    def test_village_ressources(self):
        valuemax = self.village.get_res_storage('wood')
        self.assertEqual(self.village.get_property_value('storage:wood'), valuemax)

        self.village.add_res('wood', - valuemax)
        self.assertEqual(self.village.get_res_total('wood'), 0)

        self.village.add_res('wood', valuemax)
        self.assertEqual(self.village.get_res_total('wood'), valuemax)
        
        self.village.add_res('wood', valuemax)
        self.assertEqual(self.village.get_res_total('wood'), valuemax)
        
    def test_village_building_level(self):
        self.village.set_building_level('townhall', 3)
        self.assertEqual(self.village.get_building_level('townhall'), 3)
        self.assertEqual(self.village.get_property_value('building:townhall'), 3)

        self.assertEqual(self.village.get_property_value('building:blank'), 0)
        self.village.add_building('blank')
        self.assertEqual(self.village.get_property_value('building:blank'), 1)
        self.village.set_building_level('blank', 3)
        self.assertEqual(self.village.get_property_value('building:blank'), 3)

    def test_village_tech(self):
        self.assertFalse(self.village.has_tech('blank'))
        self.village.add_tech('blank')
        self.assertTrue(self.village.has_tech('blank'))
      

    def test_village_costs(self):
        self.village.add_res('food', 10)
        self.village.add_res('wood', 10)

        self.assertTrue(self.village.has_available_res({ 'food' : 5, 'wood' : 5 }))
        self.assertFalse(self.village.has_available_res({ 'food' : 5, 'wood' : 15 }))

        self.village.pay_res({ 'food' : 5, 'wood' : 2})

        self.assertEqual(self.village.get_res_total('food'), 5)
        self.assertEqual(self.village.get_res_total('wood'), 8)

        self.assertFalse(self.village.has_available_res({ 'food' : 6, 'wood' : 6 }))

    def test_village_reqs(self):
        self.assertTrue(self.village.has_reqs({ 'building:townhall': kwd.exact(1) }))
        self.assertTrue(self.village.has_reqs({ 'building:farm': kwd.greater(1) }))
        self.assertFalse(self.village.has_reqs({ 'building:townhall': kwd.greater(2) }))
        self.assertFalse(self.village.has_reqs({ 'building:farm': kwd.exact(0) }))

    def test_village_task_simple(self):
        self.assertFalse(self.village.has_task('dummy/notatask'))
        self.assertFalse(self.village.has_task('dummy/notatask[0]'))
        
        tasktype = self.ruleset.get_tasktype('expedition/addwood')
        tasks.start_task(self.village, tasktype)
        self.assertTrue(self.village.has_task(tasktype.get_textid()))

    def test_village_set_property(self):
        self.village.set_property_value('policy:hours_leisure', 10)
        self.assertEqual(self.village.get_property_value('policy:hours_leisure'), 10)

        self.village.set_property_value('policy:test', 5)
        self.assertEqual(self.village.get_property_value('policy:test'), 5)

    def test_village_get_available_population(self):
        self.assertEqual(self.village.get_res_free("population"), 10)

        tasktype = self.ruleset.get_tasktype('expedition/usefive')
        
        task = models.Task.create(self.village, tasktype)
        self.village.commit_res(tasktype.get_uses(), task)
        self.assertEqual(self.village.get_res_free("population"), 5)
        
        task = models.Task.create(self.village, tasktype)
        self.village.commit_res(tasktype.get_uses(), task)
        self.assertEqual(self.village.get_res_free("population"), 0)

    def test_village_task_population_limit(self):
        tasktype = self.ruleset.get_tasktype('expedition/usefive')

        task = models.Task.create(self.village, tasktype)
        self.village.commit_res(tasktype.get_uses(), task)
        task = models.Task.create(self.village, tasktype)
        self.village.commit_res(tasktype.get_uses(), task)

        self.assertFalse(self.village.has_available_res(tasktype.get_uses()))

        self.village.refresh_from_db()
        self.assertEqual(self.village.get_res_free("population"), 0)
       
    def test_village_task_multiple_deletion(self):
        tasktype1 = self.ruleset.get_tasktype('expedition/addwood')
        tasktype2 = self.ruleset.get_tasktype('expedition/usefive')
        
        tasks.start_task(self.village, tasktype1)
        tasks.start_task(self.village, tasktype2)
        self.assertTrue(self.village.has_task(tasktype1.get_textid()))
        self.assertTrue(self.village.has_task(tasktype2.get_textid()))

        task1 = self.village.get_task(tasktype1.get_base_textid())
        tasks.remove_task(task1)
        self.assertFalse(self.village.has_task(tasktype1.get_textid()))
        self.assertTrue(self.village.has_task(tasktype2.get_textid()))

        task2 = self.village.get_task(tasktype2.get_base_textid())
        tasks.remove_task(task2)
        self.assertFalse(self.village.has_task(tasktype1.get_textid()))
        self.assertFalse(self.village.has_task(tasktype2.get_textid()))

        self.assertEqual(self.village.get_res_free('population'), 10)

    @testutils.time_based_test
    def test_task_is_finished(self, elapse_time):
        self.assertEqual(self.village.get_property_value('property:work_multiplier'), 1)
        
        tasktype = self.ruleset.get_tasktype('expedition/addwood')
        tasks.start_task(self.village, tasktype)
        task = self.village.get_task(tasktype.get_base_textid())
        self.assertFalse(task.is_finished())

        elapse_time(4)
        task.refresh_from_db()
        self.assertFalse(task.is_finished())

        elapse_time(4)
        task.refresh_from_db()
        self.assertFalse(task.is_finished())
        
        elapse_time(4)
        task.refresh_from_db()
        self.assertTrue(task.is_finished())

    @testutils.time_based_test
    def test_task_current_completion(self, elapse_time):
        self.assertEqual(self.village.get_property_value('property:work_multiplier'), 1)
        
        tasktype = self.ruleset.get_tasktype('expedition/addwood')
        tasks.start_task(self.village, tasktype)
        task = self.village.get_task(tasktype.get_base_textid())
        self.assertEqual(task.get_current_completion(), 0)

        elapse_time(5)
        task.refresh_from_db()
        self.assertEqual(task.get_current_completion(), 5)

        elapse_time(5)
        task.refresh_from_db()
        self.assertEqual(task.get_current_completion(), 10)

    def test_event_save_and_load(self):
        eventtype = self.ruleset.get_eventtype("basicevent")
        models.Event.create(hometown = self.village,
                     eventtype = eventtype, 
                     context = { "blah" : 2, "testparam" : 5 },
                     time = timezone.now())

        event = models.Event.objects.get(hometown = self.village) 
        self.assertEqual(event.get_context()["blah"], 2)
        self.assertEqual(event.textid, eventtype.get_textid())
        self.assertEqual(event.hometown.pk, self.village.pk)
        self.assertEqual(event.unread, True)
