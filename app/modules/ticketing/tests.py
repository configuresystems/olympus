from app import db
from app.testing import BaseTestCase
from app.core.auth.tests import AuthTestTemplates
from .models import Ticket, TicketResponse
from flask import url_for
import json
import base64

class TicketTestTemplates(BaseTestCase):
    def create_ticket(self, username='admin', password='admin',
                      title='testing', department='ops', account='fubar',
                      user_id=1, ticket_id=1, public='open'):

        response = self.client.post(
                url_for('ticketing.new'),
                headers={"Authorization": 'Basic ' + \
                        base64.b64encode(username+":"+password)},
                data=json.dumps({'title': title,
                     'department': department,
                     'account': account,
                     'responses':{
                          'user_id': user_id,
                          'ticket_id': ticket_id,
                          'public': public
                          }
                     }),
                content_type='application/json')
        return response

    def update_ticket(self, username='admin', password='admin',
                      user_id=1, ticket_id=1, public='updated', id=1):

        response = self.client.post(
                url_for('ticketing.update', id=id),
                headers={"Authorization": 'Basic ' + \
                        base64.b64encode(username+":"+password)},
                data=json.dumps({
                      'user_id': user_id,
                      'ticket_id': ticket_id,
                      'public': public
                      }
                     ),
                content_type='application/json')
        return response

    def get_ticket_by_id(self, id=1, username='admin', password='admin'):
        response = self.client.get(
                url_for('ticketing.get', id=id),
                headers={"Authorization": 'Basic ' + \
                        base64.b64encode(username+":"+password)},
                content_type='application/json')
        return response


class TicketTests(TicketTestTemplates, AuthTestTemplates):

    def setUp(self):
        db.create_all()
        self.create_admin()

    def test_db_can_create(self):
        ticket = Ticket.create(
                title='testing',
                department='ops',
                account='fubar inc'
                )
        ticket = Ticket.get(1)
        self.assertEqual('testing', ticket.title)

    def test_ticket_can_create(self):

        with self.client:
            response = self.create_user()
            self.assertEqual('test', response.json.get('username'))
            self.assertStatus(response, 201)

            response = self.create_ticket()
            self.assertStatus(response, 201)

    def test_ticket_can_update(self):

        with self.client:
            response = self.create_user()
            self.assertEqual('test', response.json.get('username'))
            self.assertStatus(response, 201)

            response = self.create_ticket()
            self.assertStatus(response, 201)
            response = self.update_ticket()
            self.assertStatus(response, 201)
            response = self.get_ticket_by_id(id=response.json.get('ticket_id'))
            self.assertStatus(response, 200)
            self.assertEqual(2, len(response.json['ticket']['responses']))

    def test_ticket_can_select(self):

        with self.client:
            response = self.create_user()
            self.assertEqual('test', response.json.get('username'))
            self.assertStatus(response, 201)
            response = self.create_ticket()
            self.assertStatus(response, 201)
            response = self.get_ticket_by_id(id=response.json.get('id'))


