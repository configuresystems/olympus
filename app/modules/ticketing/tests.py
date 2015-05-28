from app.testing import BaseTestCase
from .models import Ticket, TicketResponses
from flask import url_for
import json
import base64


class TicketTests(BaseTestCase):

    def test_db_can_create(self):

        ticket = Ticket.create(title='testing',department='ops',account='fubar inc')
        ticket = Ticket.get(1)
        self.assertEqual('testing', ticket.title)

    def test_ticket_can_create(self):

        with self.client:
            response = self.client.post(
                    url_for('auth.new_user'),
                    data=json.dumps(
                        {"username": "testing",
                         "password": "testing"
                         }), content_type='application/json')
            self.assertEqual('testing', response.json.get('username'))
            self.assertStatus(response, 201)

            response = self.client.get(
                    url_for('auth.get_auth_token'),
                    headers={"Authorization": 'Basic ' + \
                            base64.b64encode("testing:testing")},
                    content_type='application/json')
            token = response.json.get('token')

            response = self.client.post(
                    url_for('ticketing.new_ticket'),
                    headers={"Authorization": 'Basic ' + \
                            base64.b64encode("testing:testing")},
                    data=json.dumps({'title': 'testing',
                         'department': 'ops',
                         'account':'fubar inc',
                         'responses':{
                              'created_by': 'testing',
                              'parent_id': 1,
                              'public': 'open'
                              }

                         }),
                    content_type='application/json')
            self.assertStatus(response, 201)

    def test_ticket_can_select(self):

        with self.client:
            response = self.client.post(
                    url_for('auth.new_user'),
                    data=json.dumps(
                        {"username": "testing",
                         "password": "testing"
                         }), content_type='application/json')
            self.assertEqual('testing', response.json.get('username'))
            self.assertStatus(response, 201)

            response = self.client.get(
                    url_for('auth.get_auth_token'),
                    headers={"Authorization": 'Basic ' + \
                            base64.b64encode("testing:testing")},
                    content_type='application/json')
            token = response.json.get('token')

            response = self.client.post(
                    url_for('ticketing.new_ticket'),
                    headers={"Authorization": 'Basic ' + \
                            base64.b64encode("testing:testing")},
                    data=json.dumps({'title': 'testing',
                         'department': 'ops',
                         'account':'fubar inc',
                         'responses':{
                              'created_by': 'testing',
                              'parent_id': 1,
                              'public': 'open'
                              }

                         }),
                    content_type='application/json')
            self.assertStatus(response, 201)
            response = self.client.get(
                    url_for('ticketing.get_ticket', id=1),
                    headers={"Authorization": 'Basic ' + \
                            base64.b64encode("testing:testing")},
                    content_type='application/json')

#    def test_user_can_generate_token(self):
#
#        with self.client:
#            response = self.client.post(
#                    url_for('auth.new_user'),
#                    data=json.dumps(
#                        {"username": "testing",
#                         "password": "testing"
#                         }), content_type='application/json')
#            self.assertEqual('testing', response.json.get('username'))
#
#            response = self.client.get(
#                    url_for('auth.get_auth_token'),
#                    headers={"Authorization": 'Basic ' + \
#                            base64.b64encode("testing:testing")},
#                    content_type='application/json')
#            self.assert200(response)
#
#    def test_user_can_generate_token(self):
#
#        with self.client:
#            response = self.client.post(
#                    url_for('auth.new_user'),
#                    data=json.dumps(
#                        {"username": "testing",
#                         "password": "testing"
#                         }), content_type='application/json')
#            self.assertEqual('testing', response.json.get('username'))
#
#            response = self.client.get(
#                    url_for('auth.get_auth_token'),
#                    headers={"Authorization": 'Basic ' + \
#                            base64.b64encode("testing:iwillfail")},
#                    content_type='application/json')
#            self.assertStatus(response, 401)
#            self.assertEqual('Invalid Authorization', response.json.get('message'))
