import sys
sys.path.append('/var/www/hvsi.ca_devel/')
import os
os.chdir('/var/www/hvsi.ca_devel/')
from bottle import route, default_app, send_file
import bottle
bottle.debug(True)
from controller import *
application = default_app()
