from app import app, auth
from app.core.auth.models import User
from app.core.api.templates import APITemplate
from app.modules.ticketing.models import Ticket, TicketResponse
from .models import Monitor, MonitorResponse, Device, Region, State
from flask import Blueprint, g, jsonify, abort, url_for, request
from sqlalchemy import inspect
import datetime


template = APITemplate()
module = Blueprint('monitoring', __name__)


@module.route('/<int:id>', methods=['GET'])
def get(id):
    template.model = Monitor
    return template.get(id)

@module.route('/', methods=['GET'])
@module.route('/list', methods=['GET'])
def get_list():
    template.model = Monitor
    return template.get_list()


app.register_blueprint(module, url_prefix='/monitoring')
