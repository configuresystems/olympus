from app import app, auth
from app.core.auth.models import User, Role
from flask import Blueprint, g, jsonify, abort, url_for, request
import datetime

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
def new_user():
    required = ['username', 'password']
    req = request.json
    password = req['password']
    del req['password']
    if req['username'] is None or password is None:
        abort(400)
    if User.query.filter_by(username=req['username']).first() is not None:
        abort(400)
    req['created_on'] = datetime.datetime.utcnow()
    user = User(**req)
    user.hash_password(password)
    user.save()
    g.user = user
    return (jsonify(username = user.username), 201,
            {'Location': url_for('auth.get_user', id=user.id, _external=True)})

@module.route('/<int:id>')
@auth.login_required
def get_user(id):
    user = User.get(id)
    if not user:
        abort(400)
    return jsonify(user = user.get_public())

@module.route('/', methods=['GET'])
@module.route('/list', methods=['GET'])
@auth.login_required
def get_users():
    user_list = []
    users = User.query.all()
    for user in users:
        user_list.append(user.get_public())
    if not user:
        abort(400)
    return jsonify(users = user_list)

@module.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

app.register_blueprint(module, url_prefix='/users')
