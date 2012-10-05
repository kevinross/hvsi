#!/usr/bin/env python
import bottle
from controller import *
if __name__ == '__main__':
        from flup.server.fcgi import WSGIServer
        WSGIServer(bottle.default_app()).run()
