from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.login import LoginManager, current_user
from flask import Flask


# instantiate Flask so that we may use it!
app = Flask(__name__)

# Set our application constants via a config.py object
app.config.from_object('config.DevConfiguration')
login_manager = LoginManager(app)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# Import our master views file
from app import views
from app.core.database import models
db.create_all()

from app.core import logger
