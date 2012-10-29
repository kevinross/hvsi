#!/usr/bin/env python
import os, sys, time
if os.path.exists('app'):
	os.chdir('app')
	sys.path.append('.')
# set the timezone!
os.environ['TZ'] = 'America/Toronto'
time.tzset()

import bottle
from controller import *
from paste.exceptions.errormiddleware import ErrorMiddleware
if __name__ == '__main__':
        from flup.server.fcgi import WSGIServer
        app = bottle.default_app()
        app.catchall = False
        app = ErrorMiddleware(app, 
        					  debug=False,
        					  error_log=os.path.expanduser('~/public_html/hvsi/app/errors'),
        					  from_address='errors@hvsi.ca',
        					  error_email='r0ssar00@gmail.com',
        					  smtp_server='smtp.gmail.com',
        					  error_subject_prefix='HvsI Error',
        					  smtp_username='errors@hvsi.ca',
        					  smtp_password='error_reporter')
        WSGIServer(app).run()
