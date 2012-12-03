from bottle import view, route, request, response, static_file as send_file, redirect
import bottle, os, sys, datetime, urlimport
from settings import instanceconfig
import pkg_resources
# all the pages
static_root = os.getcwd()
from database import *
bottle.debug(instanceconfig.debug)
def valid_creds(user, passw):
	u = Account.from_username(user)
	if not u:
		return False
	return u.hashed_pass == passw or u.verify_pass(passw)
def set_cookie(i, as_needed=False):
	# if already set and more than 5 seconds away from expiring, don't reset it
	if as_needed and i.skey in request.cookies and datetime.datetime.now() + datetime.timedelta(0, 5) < i.expires:
		return
	response.set_cookie('session', i.skey, path="/", max_age=i.ttl)
def get_session():
	if 'session' in request.params or 'session' in request.cookies:
		try:
			info = Session.grab(request.params.get('session',None) or request.cookies.get('session',None))
		except IndexError, e:
			info = Session()
			request.params['session'] = info.skey
	else:
		info = Session()
		request.params['session'] = info.skey
	info.update_expires()
	set_cookie(info, as_needed=True)
	return info
def seterr(p, s):
	get_session().error = s
	redirect(p, 303)
# hack the Request __init__
class Request_Auth():
	def __init__(self, *args, **kwargs):
		self.logged_in = False
		self.user = None
		self.admin = False
		self.station = False
		self.player = False
		self.session = None
bottle.Request.__bases__+=(Request_Auth,)
bottle.request.logged_in = False
def error(code):
	raise bottle.HTTPError(code, bottle.HTTP_CODES[code])
def logged_in():
	return hasattr(request, 'logged_in') and request.logged_in

import basics, blog, gameops, user, admin, api
if not instanceconfig.statichost:
	import static
# catch all perm-redirect to make slashless
@route('/:page#.+#/')
def redir(page):
	redirect('/' + page, 301)