#!flask/bin/python
import os
import sys
print os.path.dirname(__file__)
sys.path.append(os.path.dirname(__file__))
activate_this = "/home/flask/application/flask/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))
from app import app as application
application.debug = True
