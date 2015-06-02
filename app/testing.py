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

