from app.testing import BaseTestCase
from app.core.auth.tests import AuthTestTemplates
from .models import Ticket, TicketResponse
from flask import url_for
import json
import base64

class TicketTestTemplates(BaseTestCase):
    def create_ticket(self, username='test', password='unittest',
                      title='testing', department='ops', account='fubar',
                      created_by='test', parent_id=1, public='open'):

        response = self.client.post(
                url_for('ticketing.new_ticket'),
                headers={"Authorization": 'Basic ' + \
                        base64.b64encode(username+":"+password)},
                data=json.dumps({'title': title,
                     'department': department,
                     'account': account,
                     'responses':{
                          'created_by': created_by,
                          'parent_id': parent_id,
                          'public': public
                          }

                     }),
                content_type='application/json')
        return response

    def get_ticket_by_id(self, id=1, username='test', password='unittest'):
        self.assertStatus(response, 201)
        response = self.client.get(
                url_for('ticketing.get_ticket', id=id),
                headers={"Authorization": 'Basic ' + \
                        base64.b64encode(username+":"+password)},
                content_type='application/json')
        return response


class TicketTests(TicketTestTemplates, AuthTestTemplates):

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

    def test_ticket_can_select(self):

        with self.client:
            response = self.create_user()
            self.assertEqual('test', response.json.get('username'))
            self.assertStatus(response, 201)
            response = self.create_ticket()
            self.assertStatus(response, 201)


