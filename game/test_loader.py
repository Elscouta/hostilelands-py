from django.test import TestCase

from game import loader

class LoaderTests(TestCase):
    def setUp(self):
        pass

    def test_get_tasktype_plain(self):
        loader.load_gamedata("gamedata.test")

        tasktype = loader.get_ruleset().get_tasktype("expedition/addwood")
        self.assertEqual(tasktype.get_base_textid(), "expedition/addwood")
        self.assertEqual(tasktype.get_textid(), "expedition/addwood")

    def test_get_tasktype_params(self):
        loader.load_gamedata("gamedata.test")

        tasktype = loader.get_ruleset().get_tasktype("job/farmer[workers=5]")
        self.assertEqual(tasktype.get_base_textid(), "job/farmer")
        self.assertEqual(tasktype.get_param("workers"), 5)

    def test_get_tasktype_altered(self):
        loader.load_gamedata("gamedata.test")
        
        tasktype = loader.get_ruleset().get_tasktype_altered("job/farmer[workers=4]", { "workers": 5 })
        self.assertEqual(tasktype.get_param("workers"), 5)
    

