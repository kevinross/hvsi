import database as db
import bottle, re
from i18n import i18n
import calendar
def static(path):
	return '//static.%s/%s' % (bottle.request.environ['HTTP_HOST'], path.lstrip('/'))