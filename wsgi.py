from bottle import view, route, request, response, static_file as send_file, redirect
import bottle, os, sys, datetime, error_page, urlimport
# all the pages
static_root = os.getcwd()
try:
	from settings import instanceconfig
	import controller
except:
	import config_app
	bottle.default_app().mount('/setup', config_app.app)
from bottle import default_app
from werkzeug.debug import DebuggedApplication
default_app().catchall = False
application = DebuggedApplication(default_app(), evalex=True)
