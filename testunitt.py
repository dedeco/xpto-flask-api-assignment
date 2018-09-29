import os
import json
import unittest

from web.api.app import app
from web.api.client import *

from base64 import b64encode

class Step1TestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_by_auth_sucess(self):

        headers = {
            'Authorization': 'Basic %s' % b64encode(b"dedeco:bmat").decode("ascii")
        }

        resp = self.app.get('/login', headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

        content = json.loads(resp.get_data(as_text=True))
        expected = True if content.get('token') else False

        self.assertEqual(True, expected)

    def test_by_auth_wrong_pass(self):

        headers = {
            'Authorization': 'Basic %s' % b64encode(b"dedeco:000000").decode("ascii")
        }

        resp = self.app.get('/login', headers=headers)
        self.assertEqual(resp.status_code, 401)


    def test_by_auth_user_not_exists(self):

        headers = {
            'Authorization': 'Basic %s' % b64encode(b"000000:000000").decode("ascii")
        }

        resp = self.app.get('/login', headers=headers)
        self.assertEqual(resp.status_code, 401)

