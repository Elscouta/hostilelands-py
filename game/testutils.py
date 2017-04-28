import json
import mock
import datetime

from django.utils import timezone
from django.test import TestCase
from django.test import Client

import world
import game
from game import models,loader,villages

##
# A class to be used for test using get/post queries 
#
class ClientTestCase(world.testutils.ClientTestCase):
    def setUp(self):
        super(ClientTestCase, self).setUp()

        #
        # Basic setup
        #
        self.start_time = timezone.now()
        self.village = models.Village.objects.create(simulation_time=self.start_time)
        self.village.add_building('townhall')
        self.village.add_building('farm')
        self.village.add_res("population", 10)
        models.Property(hometown=self.village, textid='policy:hours_leisure', value=8).save()
        models.Property(hometown=self.village, textid='policy:hours_work', value=10).save()
        models.Property(hometown=self.village, textid='policy:food_allowance', value=0).save()
        self.village.save()

        #
        # Starts a client
        #
        self.client = Client()
        self.prefix = "/game/" + str(self.village.pk) + "/"


##
# A decorator for functions that wish to perform time based queries
#
def time_based_test(func):
    def patched_test(self):
        mocked_timedate = mock.create_autospec(timezone)
        mocked_timedate.now.return_value = self.village.simulation_time
    
        def elapse_time(seconds=0, milliseconds=0):
            mocked_timedate.now.return_value += datetime.timedelta(seconds=seconds, milliseconds=milliseconds)
            villages.simulate(self.village)

        game.models.timezone = mocked_timedate
        game.villages.timezone = mocked_timedate

        func(self, elapse_time)

        game.models.timezone = timezone
        game.villages.timezone = timezone

    return patched_test
