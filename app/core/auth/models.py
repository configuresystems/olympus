from app import app, db
from flask.ext.httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
from app.core.database.mixins import CRUDMixin, ASerializer


class User(CRUDMixin, ASerializer, db.Model):
    __tablename__ = 'users'
    __public__ = ('username', 'id', 'created_on', 'role',
                  'email', 'active', 'first_name', 'last_name',
                  'phone')

    username = db.Column(db.String(32), index=True)
    first_name = db.Column(db.String(48))
    last_name = db.Column(db.String(48))
    password_hash = db.Column(db.String(64))
    created_on = db.Column(db.DateTime)
    role = db.Column(db.String(16), db.ForeignKey('roles.name'))
    email = db.Column(db.String(64))
    email = db.Column(db.String(20))
    active = db.Column(db.Boolean)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=300):
        s = Serializer(app.config['SECRET_KEY'],
                expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user

    def serialize(self):
        d = ASerializer.serialize(self)
        return d

    def __repr__(self):
        return '<User %r' % (self.username)


class Role(CRUDMixin, ASerializer, db.Model):
    __tablename__ = 'roles'
    __public__ = ('id', 'name', 'users')

    name = db.Column(db.String(16))
    users = db.relationship(
            'User',
            backref='users',
            lazy='dynamic'
            )

    def __repr__(self):
        return '<Role %r' % (self.name)

