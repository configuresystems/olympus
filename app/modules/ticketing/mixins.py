from app import db
from datetime import datetime, date
#from app.core.auth.models import User
from .models import TicketResponse


class Mixin(object):
    __table_args__ = {'extend_existing': True}

    responses = db.relationship(
            'TicketResponse',
            backref='user',
            lazy='dynamic',
            )

