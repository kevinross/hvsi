import sys
sys.path.append('/var/www/hvsi.ca/')
import os
os.chdir('/var/www/hvsi.ca/')
from bottle import route, default_app, send_file
from controller import *
application = default_app()
