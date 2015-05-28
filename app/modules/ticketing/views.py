from app import app, auth
from app.core.auth.models import User
from .models import Ticket, TicketResponses
from flask import Blueprint, g, jsonify, abort, url_for, request
from sqlalchemy import inspect


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

@module.route('/', methods=['POST'])
@auth.login_required
def new_ticket():
    title = request.json.get('title')
    department = request.json.get('department')
    account = request.json.get('account')
    response = request.json.get('responses')
    del request.json['responses']
    if title is None or department is None:
        abort(400)
    if Ticket.query.filter_by(title=title).first() is not None:
        abort(400)
    ticket = Ticket.create(**request.json)
    ticket = TicketResponses.create(**response)
    return (jsonify(request.json), 201,
            {'Location': url_for('ticketing.get_ticket', id=ticket.id, _external=True)})

@module.route('/<int:id>')
@auth.login_required
def get_ticket(id):
    ticket = Ticket.get(id)
    if not ticket:
        abort(400)
    return jsonify(ticket = ticket.get_public())

app.register_blueprint(module, url_prefix='/tickets')
