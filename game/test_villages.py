import datetime
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from gamedata.common import keywords as kwd
from game import models, loader, tasks, villages, testutils
    
class ModelTests(TestCase):
    def setUp(self):
        loader.load_gamedata("gamedata.test")

        self.village = villages.create_village("test")
        self.village.set_policy("food_allowance", 0)

    @testutils.time_based_test
    def test_elapse_time(self, elapse_time):
        start_time = self.village.simulation_time

        elapse_time(10)

        self.assertTrue(self.village.simulation_time > start_time + datetime.timedelta(seconds=8, milliseconds=900))

    @testutils.time_based_test
    def test_village_production(self, elapse_time):
        prod = self.village.get_property_value('production:food')
        self.assertTrue(prod > 0)
        self.assertEqual(self.village.get_res_total('food'), 0)

        elapse_time(10)
        self.assertEqual(self.village.get_res_total('food'), prod*10)
        
        elapse_time(10)
        self.assertEqual(self.village.get_res_total('food'), prod*20)

        elapse_time(10000)
        self.assertEqual(self.village.get_res_total('food'), self.village.get_res_storage('food'))

    @testutils.time_based_test
    def test_village_production_nosimulate(self, elapse_time):
        prod = self.village.get_property_value('production:food')
        self.assertTrue(prod > 0)
        self.assertEqual(self.village.get_res_total('food'), 0)

        elapse_time(milliseconds=750)
        self.assertEqual(self.village.get_res_total('food'), 0)

