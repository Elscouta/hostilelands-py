from django.test import TestCase,RequestFactory
from django.http import JsonResponse
from django.utils import timezone

from datetime import timedelta
from mock import patch
from decimal import Decimal

from game import loader
from game import models
from game import json_views
from game import json_tasks
from game import tasks
from game import events
from game.testutils import ClientTestCase
from game.exceptions import *

class JsonTests(ClientTestCase):
    def test_storage(self):
        self.village.add_res('wood', 5)
        tasks.start_task_by_textid(self.village, 'expedition/addwood')

        data = self.getJSON("storage/")["value"]
        self.assertEqual(data['wood']['current'], 5)
        self.assertEqual(data['wood']['production'], 0)
        self.assertEqual(data['wood']['storage'], 100)
        self.assertEqual(data['population']['free'], 9)
        self.assertEqual(data['population']['current'], 10)
       
    def test_building_list(self):
        data = self.getJSON("building/list/")
        self.assertEqual(len(data["value"]), 2)

    def test_active_task_list(self):
        data = self.getJSON("task/list/actives/expedition/")
        self.assertEqual(len(data["value"]), 0)

        tasks.start_task_by_textid(self.village, "expedition/addwood")
        data = self.getJSON("task/list/actives/expedition/")
        self.assertEqual(len(data["value"]), 1)

    def test_possible_task_list(self):
        data = self.getJSON("task/list/possibles/project+farm/")
        self.assertEqual(len(data["value"]), 1)

        data = self.getJSON("task/list/possibles/project+townhall/")
        self.assertEqual(len(data["value"]), 5)
        
    def test_possible_task_list2(self):
        data = self.getJSON("task/list/possibles/expedition/")
        self.assertEqual(len(data["value"]), 3)

    def test_get_property(self):
        data = self.getJSON("property/get/policy:hours_work/")
        self.assertEqual(data["value"], 10)
    
    def test_get_property2(self):
        data = self.getJSON("property/get/building:townhall/")
        self.assertEqual(data["value"], 1)

    def test_set_property(self):
        self.postJSON("property/set/policy:hours_work/", { "value" : 6 })
        data = self.getJSON("property/get/policy:hours_work/")
        self.assertEqual(data['value'], 6) 
       
    def test_set_property_fail(self):
        self.postJSON("property/set/building:townhall/", { "value" : 2 }, expect_status=403)
        data = self.getJSON("property/get/building:townhall/")
        self.assertEqual(data['value'], 1)

    def test_events_unread(self):
        events.create_event_by_textid(self.village, "basicevent")
        events.create_event_by_textid(self.village, "basicevent")
        events.create_event_by_textid(self.village, "basicevent")
        events.create_event_by_textid(self.village, "basicevent")

        data = self.getJSON("event/list/unread/")
        self.assertEqual(len(data['value']), 4)

        self.getJSON("event/markread/{}/".format( data['value'][0] ))
        self.getJSON("event/markread/{}/".format( data['value'][0] ))
        self.getJSON("event/markread/{}/".format( data['value'][2] ))

        data = self.getJSON("event/list/unread/")
        self.assertEqual(len(data['value']), 2)

    def test_events_get(self):
        e = events.create_event_by_textid(self.village, "basicevent")

        data = self.getJSON("event/get/{}/".format(e.pk))
        self.assertHTMLEqual(data['value'], "basicmessage")
