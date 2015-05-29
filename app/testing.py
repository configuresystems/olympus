from flask.ext.testing import TestCase
from flask import url_for
from app import app, views, db
import time
import json


class BaseTestCase(TestCase):
    """Our first unittest to check the self.response code, payload type, and payload
    """
    def create_app(self):
        """Here we can set application configurations so flag our application
        as testing, in case we build verbose functions or something"""
        app.config.from_object('config.TestingConfiguration')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_user(self, username='test', password='unittest', role='admin',
                    email='test@configure.systems', active=1):
        response = self.client.post(
                url_for('auth.new_user'),
                data=json.dumps(
                    {"username": username,
                     "password": password,
                     "role": role,
                     "email": email,
                     "active": active
                     }), content_type='application/json')
        return response

    def get_token(self, username='test', password='unittest'):
        response = self.client.get(
                url_for('auth.get_auth_token'),
                headers={"Authorization": 'Basic ' + \
                        base64.b64encode(username+":"+password)},
                content_type='application/json')
        token = response.json.get('token')
        return token


