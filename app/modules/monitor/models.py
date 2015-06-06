from app import app, db
from app.core.database.mixins import CRUDMixin, ASerializer
from sqlalchemy.inspection import inspect


class Monitor(CRUDMixin, ASerializer, db.Model):
    __tablename__ = 'monitors'
    __public__ = ()
    __admin__ = ('id', 'name', 'ip', 'alert', 'responses',
                  'created')
    __member__ = __admin__
    __limited__ = ('id', 'name', 'alert')

    name = db.Column(db.String(140), index=True)
    ip = db.Column(db.String(64), index=True)
    alert = db.Column(db.Boolean, index=True)
    created = db.Column(db.DateTime)
    responses = db.relationship(
            'MonitorResponse',
            backref='monitor',
            lazy='dynamic'
            )

    def __repr__(self):
        return '<Monitor %r' % (self.name)


class MonitorResponse(CRUDMixin, ASerializer, db.Model):
    __tablename__ = 'monitorresponses'
    __public__ = ('id', 'created', 'updated', 'device_name',
                  'state_name', 'region_name', 'monitor_id',
                  'count')

    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    device_name = db.Column(db.String(16), db.ForeignKey('devices.name'))
    state_name = db.Column(db.String(16), db.ForeignKey('states.name'))
    region_name = db.Column(db.String(16), db.ForeignKey('regions.name'))
    monitor_id = db.Column(db.Integer, db.ForeignKey('monitors.id'))
    count = db.Column(db.Integer)

    def __repr__(self):
        return '<Monitor Resp %r' % (self.id)


class Region(CRUDMixin, ASerializer, db.Model):
    __tablename__ = 'regions'
    __public__ = ('id', 'created', 'ip', 'name', 'zone')

    created = db.Column(db.DateTime)
    ip = db.Column(db.String(64), index=True)
    name = db.Column(db.String(140))
    zone = db.Column(db.String(140))


class Device(CRUDMixin, ASerializer, db.Model):
    __tablename__ = 'devices'
    __public__ = ('id', 'created', 'name', 'responses')

    created = db.Column(db.DateTime)
    name = db.Column(db.String(140))
    responses = db.relationship(
            'MonitorResponse',
            backref='device',
            lazy='dynamic'
            )

class State(CRUDMixin, ASerializer, db.Model):
    __tablename__ = 'states'
    __public__ = ('id', 'created', 'name', 'responses')

    created = db.Column(db.DateTime)
    name = db.Column(db.String(140))
    responses = db.relationship(
            'MonitorResponse',
            backref='state',
            lazy='dynamic'
            )
