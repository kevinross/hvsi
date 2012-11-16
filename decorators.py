from bottle import view, request, redirect
from controller import error, get_session, set_cookie
from database import *
import i18n
__all__ = ['mview','lang','allow_auth','require_auth','require_cond','require_role','require_user']
# decorator that automatically gives the "page" variable to templates
def mview(view_name):
	def tview(func):
		@view(view_name)
		def view_func(*args, **kwargs):
			val = func(*args, **kwargs)
			if val is not None and isinstance(val, dict) and 'page' not in val:
				val['page'] = view_name
			return val
		return view_func
	return tview
# decorator that denies access to anon
def require_auth(func):
	def auth(*args, **kwargs):
		def denied(*args, **kwargs):
			error(401)
		if 'session' not in request.params and 'session' not in request.cookies and 'username' not in request.params and not request.auth:
			return denied(*args, **kwargs)
		if not request.logged_in:
			return denied(*args, **kwargs)
		func_dict = func(*args, **kwargs)
		return func_dict
	return auth
def allow_auth(func):
	def auth(*args, **kwargs):
		info = get_session()
		setattr(request, 'logged_in', False)
		setattr(request, 'admin', None)
		setattr(request, 'station', None)
		setattr(request, 'player', None)
		setattr(request, 'user', None)
		setattr(request, 'session', info)
		if not info:
			return func(*args, **kwargs)
		if not info.user:
			return func(*args, **kwargs)
		request.user = info.user
		request.admin = isinstance(request.user, Admin)
		request.station = isinstance(request.user, Station)
		request.player = isinstance(request.user, Player)
		request.logged_in = True
		if request.station:
			info.ttl = 5*24*60*60
			info.update_expires()
			set_cookie(info)
		# force Players to read the eula if they haven't already
		if 'eula' not in request.path and request.player and not (request.user.liability and request.user.safety):
		#				for i in ('liability', 'safety'):
		#					response.set_cookie(i+'_read', '', path='/')
			redirect('/eula', 303)
		func_dict = func(*args, **kwargs)
		if func_dict and isinstance(func_dict, dict):
			if '/tag/' not in request.path:
				func_dict['user'] = request.user
		return func_dict
	return auth
# a decorator to automatically set the lang for pages, prefer cookies
def lang(func):
	def lang(*args, **kwargs):
		i = get_session()
		if 'lang' in request.params:
			lang = request.params['lang']
			if i.user:
				i.user.language = lang
		elif hasattr(request, 'user') and request.logged_in:
			lang = request.user.language
		else:
			lang = i.language
		i.language = lang
		func_dict = func(*args, **kwargs)
		if func_dict is not None and isinstance(func_dict, dict):
			func_dict['lang'] = lang
			if request.method == 'GET':
				func_dict['request'] = request
				func_dict['started'] = Game.is_started
			request.environ['i18n'] = func_dict.get('i18n',i18n.i18n)
		return func_dict
	return lang
# decorator that whitelists access based on roles
def require_role(*roles):
	def wrapper(func):
		def auth(*args, **kwargs):
			def denied(*args, **kwargs):
				error(401)
			if request.user.__class__ not in roles:
				return denied(*args, **kwargs)
			return func(*args, **kwargs)
		return auth
	return wrapper
# decorator that blacklists access based on roles
def deny_role(*roles):
	def wrapper(func):
		def auth(*args, **kwargs):
			def denied(*args, **kwargs):
				error(401)
			if request.user.__class__ in roles:
				return denied(*args, **kwargs)
			return func(*args, **kwargs)
		return auth
	return wrapper
def require_user(*users):
	def wrapper(func):
		def auth(*args, **kwargs):
			def denied(*args, **kwargs):
				error(401)
			if request.user.username not in users:
				return denied(*args, **kwargs)
			return func(*args, **kwargs)
		return auth
	return wrapper
def require_cond(cond):
	def wrapper(func):
		def auth(*args, **kwargs):
			def denied(*args, **kwargs):
				error(401)
			if callable(cond) and cond() or not callable(cond) and cond:
				return func(*args, **kwargs)
			else:
				return denied(*args, **kwargs)
		return auth
	return wrapper