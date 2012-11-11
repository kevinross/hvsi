import database as db
import bottle, re, os, simplejson
from i18n import i18n
import calendar, datetime as datetime
def static(path):
	host_parts = bottle.request.environ['HTTP_HOST'].split('.')
	host = '.'.join(['static',host_parts[-2],host_parts[-1]])
	return '//%s/%s' % (host, path.lstrip('/'))