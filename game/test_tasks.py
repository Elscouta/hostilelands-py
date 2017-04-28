from django.test import TestCase
from django.utils import timezone

from datetime import timedelta

from game.exceptions import *
from game import tasks
from game import models
from game import testutils
from game import loader
from game import villages

class TasksTests(TestCase):
    def setUp(self):
        loader.load_gamedata("gamedata.test")

        self.village = villages.create_village("test")
        self.village.set_policy("food_allowance", 0)

        self.ruleset = self.village.get_ruleset()

    def test_simple_start_and_remove(self):
        tasktype = self.ruleset.get_tasktype("expedition/addwood")
        
        tasks.start_task(self.village, tasktype)
        self.assertTrue(self.village.has_task('expedition/addwood'))

        task = self.village.get_task('expedition/addwood')
        tasks.remove_task(task)
        self.assertFalse(self.village.has_task('expedition/addwood')) 

    @testutils.time_based_test
    def test_start_and_finish(self, elapse_time):
        tasktype = self.ruleset.get_tasktype("expedition/addwood")
        
        tasks.start_task(self.village, tasktype)
        self.assertTrue(self.village.has_task('expedition/addwood'))

        elapse_time(5)
        
        task = self.village.get_task('expedition/addwood')
        with self.assertRaises(GameRulesViolation):
            tasks.complete_task(task)
        
        self.assertTrue(self.village.has_task('expedition/addwood')) 
        self.assertEqual(self.village.get_res_total('wood'), 0)

        elapse_time(7)
        
        task = self.village.get_task('expedition/addwood')
        tasks.complete_task(task)

        self.assertFalse(self.village.has_task('expedition/addwood')) 
        self.assertEqual(self.village.get_res_total('wood'), 1)
        
        with self.assertRaises(models.Task.DoesNotExist):
            task = self.village.get_task('expedition/addwood')

    def test_update_task(self):
        tasktype = self.ruleset.get_tasktype("job/farmer[workers=3]")
        self.village.set_building_level("farm", 3)

        tasks.start_task(self.village, tasktype)
        
        task = self.village.get_task("job/farmer")
        tasks.update_task(task, { "workers" : 5 })
        
        task = self.village.get_task("job/farmer")
        self.assertEqual(task.get_param("workers"), 5)

    def test_insufficient_ressources(self):
        tasktype = self.ruleset.get_tasktype("upgradebuilding/farm[level=2,]")

        with self.assertRaises(InsufficientRessourcesViolation):
            tasks.start_task(self.village, tasktype)
    
    @testutils.time_based_test
    def test_parameterized_start(self, elapse_time):
        tasktype = self.ruleset.get_tasktype("upgradebuilding/farm[level=2,]")

        self.village.add_res("food", 100)
        self.village.add_res("wood", 100)

        tasks.start_task(self.village, tasktype)

        elapse_time(3600)

        task = self.village.get_task('upgradebuilding/farm')
        tasks.complete_task(task)

        with self.assertRaises(models.Task.DoesNotExist):
            task = self.village.get_task('upgradebuilding/farm')
        
        self.assertEqual(self.village.get_property_value("building:farm"), 2)

    @testutils.time_based_test
    def test_continuous_task_one(self, elapse_time):
        tasktype = self.ruleset.get_tasktype("job/farmer[workers=1]")

        with self.assertRaises(GameRulesViolation):
            tasks.start_task(self.village, tasktype)

        self.village.set_building_level("farm", 3)

        tasks.start_task(self.village, tasktype)

        elapse_time(60)

        self.assertEqual(self.village.get_res_total("food"), 24)

        task = self.village.get_task("job/farmer")
        
        with self.assertRaises(GameRulesViolation):
            tasks.complete_task(task)

        tasks.remove_task(task)
        
        elapse_time(60)

        self.assertEqual(self.village.get_res_total("food"), 42)

    @testutils.time_based_test
    def test_continuous_task_multiples(self, elapse_time):
        tasktype = self.ruleset.get_tasktype("job/farmer[workers=10]")
        self.village.set_building_level("farm", 3)

        tasks.start_task(self.village, tasktype)

        elapse_time(60)

        self.assertEqual(self.village.get_res_total("food"), 78)

