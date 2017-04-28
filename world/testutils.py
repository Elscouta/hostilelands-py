import json

from django.test import TestCase
from django.test import Client

from game import loader
##
# A class to be used for test using get/post queries 
#
class ClientTestCase(TestCase):
    def setUp(self):
        loader.load_gamedata("gamedata.test")

        #
        # Starts a client
        #
        self.client = Client()
        self.prefix = "/"

    def assert200(self, url):
        self.assertStatusCode(url, 200)
    
    def assert404(self, url):
        self.assertStatusCode(url, 404)

    def assertStatusCode(self, url, status_code):
        resp = self.client.get(self.prefix + url)
        self.assertEqual(resp.status_code, status_code, resp.content)

    def assert200_post(self, url, data):
        self.assertStatusCode_post(url, data, 200)
        
    def assert404_post(self, url, data):
        self.assertStatusCode_post(url, data, 404)

    def assertStatusCode_post(self, url, data, status_code):
        resp = self.client.post(self.prefix + url, json.dumps(data), content_type="application/json")
        self.assertEqual(resp.status_code, status_code, resp.content)

    def getJSON(self, url, expect_status=200):
        resp = self.client.get(self.prefix + url)
        self.assertEqual(resp.status_code, expect_status, resp.content)
        return json.loads(resp.content.decode('ascii'))

    def postJSON(self, url, data, expect_status=200):
        resp = self.client.post(self.prefix + url, json.dumps(data), content_type="application/json")
        self.assertEqual(resp.status_code, expect_status, resp.content)
        return json.loads(resp.content.decode('ascii'))
    
    def postForm(self, url, data, expect_status=302, expect_redirect=None):
        resp = self.client.post(self.prefix + url, data)
        self.assertEqual(resp.status_code, expect_status, resp.content)

        if (expect_redirect):
            assert(expect_status == 302)
            self.assertRedirects(resp, expect_redirect)

        return resp.content

