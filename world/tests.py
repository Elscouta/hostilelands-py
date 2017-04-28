from django.test import TestCase

from game import loader
from game.models import Village

from world import testutils

# Create your tests here.
class Tests(testutils.ClientTestCase):
        
    def test_index(self):
        self.assert200("")

    def test_newvillage_initial(self):
        self.assert200("newvillage/")

    def test_newvillage_error(self):
        self.assert200_post("newvillage/", {})

    def test_newvillage_success(self):
        self.postForm("newvillage/", { "name" : "test" })
        self.assertEqual(Village.objects.count(), 1)

        v = Village.objects.get()
        self.assertEqual(v.get_building_level("townhall"), 1)
        self.assertEqual(v.get_res_total("population"), 10)
