from django.test import TestCase
from django.utils import timezone

from decimal import Decimal

from gamedata.common import keywords as kwd
from game import models, loader, tasks, villages, testutils, events

class EventTests(TestCase):
    def setUp(self):
        loader.load_gamedata("gamedata.test")

        self.village = villages.create_village("test")
        self.village.set_policy("food_allowance", 0)

    def test_templated_event(self):
        e = events.create_event_by_textid(self.village, "templatedevent")
        self.assertHTMLEqual(events.get_message(e), "value")

    @testutils.time_based_test
    def test_immediate_starvation_event(self, elapse_time):
        self.village.set_policy("food_allowance", 2000)

        elapse_time(10)

        self.assertEqual(self.village.get_res_total("population"), 0)
        self.assertTrue(self.village.get_res_total("food") > 0.99)

    @testutils.time_based_test
    def test_delayed_starvation_event(self, elapse_time):
        self.village.add_res("food", Decimal('0.5'))
        self.village.set_policy("food_allowance", 20)

        elapse_time(10)
        
        self.assertEqual(self.village.get_res_total("population"), 5)
        self.assertEqual(self.village.get_res_total("food"), 0)
