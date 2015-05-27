# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join


_cwd = dirname(abspath(__file__))


class BaseConfiguration(object):
    """This is the applications base configuration object.
    It will contain all of the DEFAULT constant values for
    our applications.  Every configuration object will inherit
    this.

    """

    DEBUG = True
    TESTING = False

    SECRET_KEY = 'A11 y0uR b453 are BELONG 70 US!'

    ADMINS = frozenset(['youremail@yourdomain.com'])

    THREADS_PER_PAGE = 8

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "th1S#i5 How we_d0 3T."

    DATABASE = 'app.db'
    DATABASE_PATH = join(_cwd, DATABASE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH


class DevConfiguration(BaseConfiguration):
    """This configuration should be used and tailored to help
    limit the frustrations of debugging

    {{ params }}
    DEBUG = False"""
    DATABASE = 'dev.db'
    DATABASE_PATH = join(_cwd, DATABASE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
    DEBUG = True


class TestingConfiguration(BaseConfiguration):
    """This configuration should be used and tailored for testing
    the application.

    {{ params }}
    TESTING = True"""
    TESTING = True
    DATABASE = 'tests.db'
    DATABASE_PATH = join(_cwd, DATABASE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

