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
if __name__ == '__main__':
        from flup.server.fcgi import WSGIServer
        WSGIServer(bottle.default_app()).run()
