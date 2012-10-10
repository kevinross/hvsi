#!/usr/bin/env python
import os, sys
if os.path.exists('app'):
	os.chdir('app')
	sys.path.append('.')
import bottle
from controller import *
if __name__ == '__main__':
        from flup.server.fcgi import WSGIServer
        WSGIServer(bottle.default_app()).run()
