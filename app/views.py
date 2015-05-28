"""So that we can modularize our application, we will use this as our
our master file for application endpoints"""
from app import app, login_manager
from flask import Blueprint
from app.core import errors
from app.core.auth.views import module as auth
from app.modules.ticketing.views import module as ticketing
