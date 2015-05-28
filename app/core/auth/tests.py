from app.testing import BaseTestCase
from .models import User
from flask import url_for
import json
import base64


class AuthTests(BaseTestCase):

    def test_db_can_create(self):

        user = User(username='testing')
        user.hash_password('testing')
        user.save()
        user = User.get(1)
        self.assertEqual('testing', user.username)

    def test_user_can_create(self):

        with self.client:
            response = self.client.post(
                    url_for('auth.new_user'),
                    data=json.dumps(
                        {"username": "testing",
                         "password": "testing"
                         }), content_type='application/json')
            self.assertEqual('testing', response.json.get('username'))
            self.assertStatus(response, 201)

    def test_user_can_generate_token(self):

        with self.client:
            response = self.client.post(
                    url_for('auth.new_user'),
                    data=json.dumps(
                        {"username": "testing",
                         "password": "testing"
                         }), content_type='application/json')
            self.assertEqual('testing', response.json.get('username'))

            response = self.client.get(
                    url_for('auth.get_auth_token'),
                    headers={"Authorization": 'Basic ' + \
                            base64.b64encode("testing:testing")},
                    content_type='application/json')
            self.assert200(response)

    def test_user_can_generate_token(self):

        with self.client:
            response = self.client.post(
                    url_for('auth.new_user'),
                    data=json.dumps(
                        {"username": "testing",
                         "password": "testing"
                         }), content_type='application/json')
            self.assertEqual('testing', response.json.get('username'))

            response = self.client.get(
                    url_for('auth.get_auth_token'),
                    headers={"Authorization": 'Basic ' + \
                            base64.b64encode("testing:testing")},
                    content_type='application/json')
            self.assert200(response)
            token = response.json.get('token')

    def test_user_fails_generate_token(self):

        with self.client:
            response = self.client.post(
                    url_for('auth.new_user'),
                    data=json.dumps(
                        {"username": "testing",
                         "password": "testing"
                         }), content_type='application/json')
            self.assertEqual('testing', response.json.get('username'))

            response = self.client.get(
                    url_for('auth.get_auth_token'),
                    headers={"Authorization": 'Basic ' + \
                            base64.b64encode("testing:iwillfail")},
                    content_type='application/json')
            self.assertStatus(response, 401)
            self.assertEqual('Invalid Authorization', response.json.get('message'))
