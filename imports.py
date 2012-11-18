from settings import instanceconfig
import database as db
import bottle, re, os, simplejson
i18n = bottle.request.environ['i18n']
import calendar, datetime as datetime
def static(path):
	if instanceconfig.statichost == '[builtin]':
		return path
	return '//%s/%s' % (instanceconfig.statichost, path.lstrip('/'))