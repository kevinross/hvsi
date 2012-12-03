from settings import instanceconfig
import bottle, re, os, simplejson
import calendar, datetime as datetime, random
def static(path):
	if not instanceconfig.statichost:
		return path
	return '//%s/%s' % (instanceconfig.statichost, path.lstrip('/'))