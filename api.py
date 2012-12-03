from decorators import *
from database import *
from sqlobject import *
from controller import error, seterr, get_session, set_cookie
import i18n, datetime, simplejson
from bottle import route, get, post, request, response, redirect
def is_allowed(klass, ids, user):
	s = get_session()
	if s.admin:
		return True
	items = klass.select(IN(klass.q.id, ids))
	if s.player:
		if klass == Player:
			# only allow players to get themselves
			if ids[0] != s.user.id:
				return False
		elif klass in (Post, Comment, Score, String):
			return True
	return False
@post('/api/resolve_objects')
@allow_auth
def resolve_objects():
	try:
		klass_name = request.json['name']
		ids = request.json['items']
	except:
		klass_name = None
		ids = None
		error(400)
	klass = globals()[klass_name]
	if not is_allowed(klass, ids):
		error(403)
	return dict(items=[x.dict for x in klass.select(IN(klass.q.id, ids))])

@post('/api/resolve_names')
@allow_auth
def resolve_names():
	try:
		ids = request.json['names']
	except:
		ids = None
		error(400)
	return dict(items=[x.username for x in Player.users])