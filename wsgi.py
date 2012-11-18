import bottle, os, sys, datetime, urlimport, time
static_root = os.getcwd()
try:
	from settings import instanceconfig
	os.environ['TZ'] = instanceconfig.timezone
	time.tzset()
	import controller
	application = bottle.default_app()
	if instanceconfig.debug:
		from werkzeug.debug import DebuggedApplication
		application.catchall = False
		application = DebuggedApplication(application, evalex=True)
	else:
		if instanceconfig.exceptionpath:
			from paste.exceptions.errormiddleware import ErrorMiddleware
			application = ErrorMiddleware(application,
										  debug=False,
										  error_log=instanceconfig.exceptionpath)
except:
	import config_app
	application = bottle.default_app()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		from bottle import run
		run(application, port=9055)
	else:
		from flup.server.fcgi import WSGIServer
		WSGIServer(application).run()