import json
from datetime import timedelta
from decimal import Decimal

from django.utils import timezone

from game import loader, models, testutils

class HttpQueriesTest(testutils.ClientTestCase):
        
    def test_shows(self):
        self.assert200("")
        self.assert200("storage/")
        self.assert200("building/show/townhall/")
        self.assert200("building/show/farm/")
        self.assert200("building/list/")
        self.assert200("task/list/possibles/farm+project/")
        self.assert200("task/list/actives/farm+project/")
        self.assert200("property/get/property:farmefficiency/")
        self.assert200("property/get/task:job/farmer/")
        self.assert200("property/get/internal[task:job/farmer:workers]:production:food/")

    def test_posts(self):
        self.assert200_post("property/set/policy:hours_work/", { 'value': 1 })
    
    def test_taskstart0(self):
        self.assert200("task/start/expedition/addwood/")
        task = self.village.get_task("expedition/addwood")
        self.assert200("task/cancel/" + str(task.pk) + "/")
        self.assert404("task/cancel/" + str(task.pk) + "/")
        self.assert404("task/end/" + str(task.pk) + "/")

    @testutils.time_based_test
    def test_taskstart1(self, elapse_time):
        self.assert200("task/start/expedition/addwood/")

        elapse_time(3600)
        task = self.village.get_task("expedition/addwood")

        self.assert200("task/end/" + str(task.pk) + "/")

    @testutils.time_based_test
    def test_taskstart2(self, elapse_time):
        self.village.add_res("food", 100)
        self.village.add_res("wood", 100)

        self.assert200("task/start/upgradebuilding/farm[level=2,]/")

        elapse_time(3600)
        task = self.village.get_task("upgradebuilding/farm")

        self.assert200("task/end/" + str(task.pk) + "/")

    @testutils.time_based_test
    def test_taskcontinuous_modif(self, elapse_time):
        self.village.set_building_level("farm", 3)
        self.assertEqual(self.village.get_res_production("food"), Decimal('0.3'))

        self.assert200("task/start/job/farmer[workers=1]/")
        self.assertEqual(self.village.get_res_production("food"), Decimal('0.4'))

        elapse_time(10)
        taskid = str(self.village.get_task("job/farmer").pk)
        self.assert200("task/addworker/"+ taskid +"/")
        self.assert200("task/addworker/"+ taskid +"/")
        self.assert200("task/addworker/"+ taskid +"/")
        self.assert200("task/addworker/"+ taskid +"/")
        self.assertEqual(self.village.get_task("job/farmer").get_param("workers"), 5)
        self.assertEqual(self.village.get_res_production("food"), Decimal('0.8'))

        elapse_time(10)
        self.assert200("task/removeworker/"+ taskid +"/")
        self.assert200("task/removeworker/"+ taskid +"/")
        self.assert200("task/removeworker/"+ taskid +"/")
        self.assertEqual(self.village.get_res_production("food"), Decimal('0.5'))
