"""So that we can modularize our application, we will use this as our
our master file for application endpoints"""
from app import app, login_manager
from app.core import errors
from app.core.auth import views

