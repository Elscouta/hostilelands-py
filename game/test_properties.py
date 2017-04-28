from django.test import TestCase
from django.utils import timezone

from decimal import Decimal

from game import models, loader, villages

class PropertyTests(TestCase):
    def setUp(self):
        loader.load_gamedata("gamedata.test")

        self.village = villages.create_village("test")
        self.village.set_policy("food_allowance", 50)

        self.ruleset = self.village.get_ruleset()

    def test_loader(self):
        self.assertTrue("property:farmefficiency" in self.ruleset.get_all_propertytypes())
        self.assertTrue("internal[policy:food_allowance]:consume:food" in self.ruleset.get_all_propertytypes())
        self.assertTrue("internal[building:farm]:production:food" in self.ruleset.get_all_propertytypes())

    def test_policies(self):
        self.assertEqual(self.village.get_property_value('policy:hours_leisure'), 6)
        self.assertEqual(self.village.get_property_value('policy:hours_work'), 10)
        self.assertEqual(self.village.get_property_value('policy:food_allowance'), 50)

    def test_property_computation(self):
        self.village.set_policy('hours_leisure', 8)
        self.village.set_policy('hours_work', 8)
        self.assertEqual(self.village.get_property_value('property:hours_rest'), 8)
        self.assertEqual(self.village.get_property_value('property:exhaustion'), 7)
        self.assertEqual(self.village.get_property_value('property:happyness'), 40)
        self.assertEqual(self.village.get_property_value('property:work_multiplier'), Decimal('0.8'))

    def test_property_internal(self):
        self.assertEqual(self.village.get_property_value('internal[building:farm]:production:food'), Decimal('0.1'))
        self.assertEqual(self.village.get_property_value('internal[policy:food_allowance]:consume:food'), Decimal('0.500'))

    def test_property_tech(self):
        self.assertEqual(self.village.get_property_value('tech:irrigation'), 0)
        self.assertEqual(self.village.get_property_value('property:farmefficiency'), 1)
        self.village.add_tech("irrigation")
        self.assertEqual(self.village.get_property_value('tech:irrigation'), 1)
        self.assertEqual(self.village.get_property_value('property:farmefficiency'), Decimal('1.25'))
        self.assertEqual(self.village.get_property_value('internal[building:farm]:production:food'), Decimal('0.125'))

    def test_property_task(self):
        self.assertEqual(self.village.get_property_value('task:expedition/addwood'), 0)
        self.assertEqual(self.village.get_property_value('task:job/farmer'), 0)
        self.assertEqual(self.village.get_property_value('internal[task:job/farmer:workers]:production:food'), 0)
        
        tasktype = self.ruleset.get_tasktype('expedition/addwood')
        models.Task.create(self.village, tasktype)
        tasktype = self.ruleset.get_tasktype('job/farmer[workers=5]')
        models.Task.create(self.village, tasktype)
        
        self.assertEqual(self.village.get_property_value('task:expedition/addwood'), 1)
        self.assertEqual(self.village.get_property_value('task:job/farmer'), 1)
        self.assertEqual(self.village.get_property_value('task:job/farmer:workers'), 5)
        self.assertEqual(self.village.get_property_value('internal[task:job/farmer:workers]:production:food'), Decimal('0.5'))
        
    def test_property_consumes(self):

        self.assertEqual(self.village.get_property_value('production:food'), Decimal('-0.4'))

    def test_property_query(self):
        
        effects = self.ruleset.get_propertytype("building:farm").get_property_effects(1, self.village)
        self.assertEqual(effects["production:food"]["base"], Decimal('0.1'))
        self.assertEqual(effects["production:food"]["actual"], Decimal('0.1'))

        effects = self.ruleset.get_propertytype("building:farm").get_property_effects(2, self.village)
        self.assertEqual(effects["production:food"]["base"], Decimal('0.2'))
        self.assertEqual(effects["production:food"]["actual"], Decimal('0.2'))

        self.village.add_tech("irrigation")
        effects = self.ruleset.get_propertytype("building:farm").get_property_effects(2, self.village)
        self.assertEqual(effects["production:food"]["base"], Decimal('0.2'))
        self.assertEqual(effects["production:food"]["actual"], Decimal('0.25'))
        
