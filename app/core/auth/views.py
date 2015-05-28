from app import app, auth
from app.core.auth.models import User
from flask import Blueprint, g, jsonify, abort, url_for, request

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

@module.route('/', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    user.save()
    g.user = user
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('auth.get_user', id=user.id, _external=True)})

@module.route('/<int:id>')
@auth.login_required
def get_user(id):
    user = User.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@module.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

app.register_blueprint(module, url_prefix='/users')
