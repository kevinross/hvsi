import sys, os
BASE=os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE)
os.chdir(BASE)
from bottle import route, default_app, send_file
from controller import *
application = default_app()
