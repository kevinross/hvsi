#from controller import *
import controller
from bottle import run, default_app
from werkzeug.debug import DebuggedApplication
default_app().catchall = False
app = DebuggedApplication(default_app(), evalex=True)
run(app, port=9055)
