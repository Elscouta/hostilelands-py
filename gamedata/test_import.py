from django.test import TestCase

class ImportTests(TestCase):
    def setUp(self):
        pass

    def test_import_test(self):
        import gamedata.test

    def test_import_standard(self):
        import gamedata.standard
