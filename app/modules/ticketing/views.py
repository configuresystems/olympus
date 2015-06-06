from app import app, auth
from app.core.auth.models import User
from app.core.api.templates import APITemplate
from .models import Ticket, TicketResponse
from flask import Blueprint, g, jsonify, abort, url_for, request
from sqlalchemy import inspect
import datetime


template = APITemplate()
module = Blueprint('ticketing', __name__)


@module.route('/create', methods=['POST'])
@auth.login_required
def new():
    template.model = Ticket
    template.required_fields(request.json)
    template.check_unique({'title':request.json.get('title')})

    if g.user.role not in ['admin','member']:
        abort(401)

    req = request.json

    created_on = req['created_on'] = datetime.datetime.utcnow()
    response = req['responses']
    del req['responses']

    ticket = Ticket.create(**req)
    response['ticket_id'] = ticket.id
    response['user_id'] = g.user.id
    response['created_on'] = created_on
    ticket_response = TicketResponse.create(**response)
    ticket = Ticket.get(ticket.id)
    return (jsonify(ticket.get_public()), 201,
            {'Location': url_for('ticketing.get', id=ticket.id, _external=True)})

@module.route('/<int:id>', methods=['PUT', 'POST'])
@auth.login_required
def update(id):
    if g.user.role not in ['admin','member']:
        abort(401)
    req = request.json
    req['created_on'] = datetime.datetime.utcnow()
    req['ticket_id'] = id
    req['user_id'] = g.user.id
    template.model = TicketResponse
    return template.update(id=id, url='ticketing.get', data=req)

@module.route('/<int:id>', methods=['GET'])
@auth.login_required
def get(id):
    template.model = Ticket
    return template.get(id)

@module.route('/', methods=['GET'])
@module.route('/list', methods=['GET'])
@auth.login_required
def get_list():
    template.model = Ticket
    return template.get_list()

app.register_blueprint(module, url_prefix='/tickets')
