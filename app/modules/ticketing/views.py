from app import app, auth
from app.core.auth.models import User
from .models import Ticket, TicketResponse
from flask import Blueprint, g, jsonify, abort, url_for, request
from sqlalchemy import inspect
import datetime


module = Blueprint('ticketing', __name__)

def make_public_ticket(ticket):
    new_ticket = {}
    for field in ticket:
        if field == 'id':
            new_ticket['uri'] = url_for(
                    'ticketing.get_ticket',
                    id=ticket['id'],
                    _external=True)
        else:
            new_ticket[field] = ticket['field']
    return new_ticket

@module.route('/create', methods=['POST'])
@auth.login_required
def new_ticket():
    if g.user.role not in ['admin','member']:
        abort(401)
    req = request.json
    created_on = req['created_on'] = datetime.datetime.utcnow()
    response = req['responses']
    del req['responses']
    if req['title'] is None or req['department'] is None:
        abort(400)
    if Ticket.query.filter_by(title=req['title']).first() is not None:
        abort(400)
    ticket = Ticket.create(**req)
    response['ticket_id'] = ticket.id
    response['user_id'] = g.user.id
    response['created_on'] = created_on
    ticket_response = TicketResponse.create(**response)
    ticket = Ticket.get(ticket.id)
    return (jsonify(ticket.get_public()), 201,
            {'Location': url_for('ticketing.get_ticket', id=ticket.id, _external=True)})

@module.route('/<int:id>', methods=['PUT', 'POST'])
@auth.login_required
def update_ticket(id):
    if g.user.role not in ['admin','member']:
        abort(401)
    req = request.json
    req['created_on'] = datetime.datetime.utcnow()
    req['ticket_id'] = id
    req['user_id'] = g.user.id
    ticket = TicketResponse.create(**req)
    return (jsonify(ticket.get_public()), 201,
            {'Location': url_for('ticketing.get_ticket', id=ticket.id, _external=True)})

@module.route('/<int:id>', methods=['GET'])
@auth.login_required
def get_ticket(id):
    ticket = Ticket.get(id)
    if not ticket:
        abort(400)
    return jsonify(ticket = ticket.get_public())

@module.route('/', methods=['GET'])
@module.route('/list', methods=['GET'])
@auth.login_required
def get_tickets():
    ticket_list = []
    tickets = Ticket.query.all()
    for ticket in tickets:
        ticket_list.append(ticket.get_public())
    if not ticket:
        abort(400)
    return jsonify(tickets = ticket_list)

app.register_blueprint(module, url_prefix='/tickets')
