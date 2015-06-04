from app.testing import BaseTestCase
from .models import User
from flask import url_for
import json
import base64


class AuthTestTemplates(BaseTestCase):

    def create_user(self, username='test', password='unittest', role='admin',
                    email='test@configure.systems', active=1,
                    first_name='first', last_name='last',
                    login_username='admin', login_password='admin'):

        response = self.client.post(
                url_for('auth.new_user'),
                headers={"Authorization": 'Basic ' + \
                        base64.b64encode(login_username+":"+login_password)},
                data=json.dumps(
                    {"username": username,
                     "password": password,
                     "first_name": first_name,
                     "last_name": last_name,
                     "role": role,
                     "email": email,
                     "active": active
                     }), content_type='application/json')
        return response

    def create_admin(self):
        admin = {'username':'admin','role':'admin','last_name':'admin',
                 'first_name':'admin','last_name':'admin',
                 'email':'admin@configure.systems'}
        user = User(**admin)
        user.hash_password('admin')
        user.save()
        user = User.get(1)
        self.assertEqual('admin', user.username)

    def create_token(self, username='admin', password='admin'):
        response = self.client.get(
                url_for('auth.get_auth_token'),
                headers={"Authorization": 'Basic ' + \
                        base64.b64encode(username+":"+password)},
                content_type='application/json')
        return response

    def get_token(self, username='admin', password='admin'):
        response = self.client.get(
                url_for('auth.get_auth_token'),
                headers={"Authorization": 'Basic ' + \
                        base64.b64encode(username+":"+password)},
                content_type='application/json')
        token = response.json.get('token')
        return token

    def make_request(self, username_or_token, url='auth.get_user',
                     password=None):
        if not password:
            auth = username_or_token + ":x"
        else:
            auth = username_or_token + ":" + password
        response = self.client.get(
                url_for(url, id=2),
                headers={"Authorization": 'Basic ' + \
                        base64.b64encode(auth)},
                content_type='application/json')
        return response


class AuthTests(AuthTestTemplates):

    def test_db_can_create(self):

        user = User(username='test')
        user.hash_password('unittest')
        user.save()
        user = User.get(1)
        self.assertEqual('test', user.username)

    def test_user_can_create(self):

        self.create_admin()

        with self.client:
            response = self.create_user()
            self.assertEqual('test', response.json.get('username'))
            self.assertStatus(response, 201)

    def test_user_can_generate_token(self):

        self.create_admin()

        with self.client:
            response = self.create_user()
            self.assertEqual('test', response.json.get('username'))

            response = self.create_token()
            self.assert200(response)

    def test_user_fails_generate_token(self):

        self.create_admin()

        with self.client:
            response = self.create_user()
            self.assertEqual('test', response.json.get('username'))
            response = self.create_token(password='iwillfail')

            self.assertStatus(response, 401)
            self.assertEqual('Invalid Authorization', response.json.get('message'))

    def test_user_can_access_user_with_user_pass(self):

        self.create_admin()

        with self.client:
            response = self.create_user()
            self.assertEqual('test', response.json.get('username'))
            response = self.make_request(username_or_token='test',
                                         password='unittest')
            self.assert200(response)
            self.assertEqual('test', response.json['user']['username'])

    def test_user_can_access_user_with_token(self):

        self.create_admin()

        with self.client:
            response = self.create_user()
            self.assertEqual('test', response.json.get('username'))

            response = self.create_token()
            token = response.json.get('token')
            response = self.make_request(username_or_token=token)

            self.assert200(response)
            self.assertEqual('test', response.json['user']['username'])

    def test_user_limited_access_user_with_token_and_role(self):

        self.create_admin()

        with self.client:
            response = self.create_user()
            self.assertEqual('test', response.json.get('username'))
            response = self.create_user(username='fooman', role='limited')
            self.assertEqual('fooman', response.json.get('username'))

            response = self.create_token(username='fooman',
                    password='unittest')
            token = response.json.get('token')
            response = self.make_request(username_or_token=token)

            self.assertStatus(response, 200)

    def test_user_limited_access_users_with_token_and_role(self):

        self.create_admin()

        with self.client:
            response = self.create_user()
            self.assertEqual('test', response.json.get('username'))
            response = self.create_user(username='fooman', role='limited')
            self.assertEqual('fooman', response.json.get('username'))

            response = self.create_token(username='fooman',
                    password='unittest')
            token = response.json.get('token')
            response = self.make_request(username_or_token=token,
                                         url='auth.get_users')
            self.assertEqual(3, len(response.json.get('users')))

            self.assertStatus(response, 200)
