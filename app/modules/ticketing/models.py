from app import app, db
from app.core.database.mixins import CRUDMixin, ASerializer
from sqlalchemy.inspection import inspect


class Ticket(CRUDMixin, ASerializer, db.Model):
    __tablename__ = 'tickets'
    __public__ = ('id', 'title', 'department', 'account', 'responses',
                  'created_on')
    __required__ = ['title', 'department']

    title = db.Column(db.String(140), index=True)
    department = db.Column(db.String(64), index=True)
    account = db.Column(db.String(64), index=True)
    created_on = db.Column(db.DateTime)
    responses = db.relationship(
            'TicketResponse',
            backref='ticket',
            lazy='dynamic'
            )

    def __repr__(self):
        return '<Ticket %r' % (self.title)


class TicketResponse(CRUDMixin, ASerializer, db.Model):
    __tablename__ = 'ticketresponses'
    __public__ = ('id', 'user_id', 'ticket_id', 'created_on',
                  'public', 'private', 'status')

    created_on = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    public = db.Column(db.String(2048))
    private = db.Column(db.String(2048))
    status = db.Column(db.String(16))

    def __repr__(self):
        return '<Ticket Resp %r' % (self.id)

