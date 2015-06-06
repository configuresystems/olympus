from app import app, auth
from app.core.api.templates import APITemplate
from app.core.auth.models import User, Role
from flask import Blueprint, g, jsonify, abort, url_for, request
import datetime

template = APITemplate()
module = Blueprint('auth', __name__)

@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@module.route('/create', methods=['POST'])
@auth.login_required
def new():
    template.access = ['admin']
    template.check_privilege()

    template.model = User
    template.required_fields(request.json)
    template.check_unique({'username':request.json['username']})

    req = request.json
    password = req['password']
    del req['password']


    req['created_on'] = datetime.datetime.utcnow()
    user = User(**req)
    user.hash_password(password)
    user.save()
    g.user = user
    return (jsonify(username = user.username), 201,
            {'Location': url_for('auth.get', id=user.id, _external=True)})

@module.route('/<int:id>')
@auth.login_required
def get(id):
    template.access = ['admin', 'member', 'limited']
    template.check_privilege()

#    user = User.get(id)
#    if g.user.role in ['limited']:
#        user.__public__ = ('username', 'created_on', 'active')

    template.model = User
    return template.get(id)

@module.route('/', methods=['GET'])
@module.route('/list', methods=['GET'])
@auth.login_required
def get_list():
    template.access = ['admin', 'member', 'limited']
    template.check_privilege()

#    for user in users:
#        if g.user.role in ['limited']:
#            user.__public__ = ('username', 'created_on', 'active')
#        user_list.append(user.get_public())
#    if not user:
#        abort(400)

    template.model = User
    return template.get_list()

@module.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

app.register_blueprint(module, url_prefix='/users')
