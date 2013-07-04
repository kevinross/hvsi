from decorators import *
from database import *
from sqlobject import *
from controller import error, seterr, get_session, set_cookie, valid_creds
import i18n, datetime, simplejson, bottle
from bottle import default_app, route, get, post, request, response, redirect, SimpleTemplate
from jsonrpc import build_routes, JSONRPC, Client, json, unjson
from functools import partial
getters = dict()

def str2class(s):
	if s in ('Admin', 'Post', 'Comment', 'DbString', 'Bounty', 'Score', 'Game', 'Account', 'Player', 'Session', 'Tag'):
		return eval(s)
	if s is 'DbString':
		return DbString

def anongetter(klass, ids):
	klass = str2class(klass)
	# for data that everyone can access
	return klass.select(IN(klass.q.id, ids))

def owngetter(klass, ids=[]):
	klass = str2class(klass)
	# for data that only the logged-in user or admin can access
	# and *only* that data
	print get_session().user
	if isinstance(get_session().user, Admin) or klass == Game:
		return list(klass.select(IN(klass.q.id, ids)))
	if klass == Player:
		return [get_session().user]
	if klass == Tag:
		return [dict(tagger=x.tagger.username,taggee=x.taggee.username) for x in Tag.for_user(get_session().user)]
	if klass == Session:
		return [get_session()]

for k in ['Post', 'Comment', 'DbString', 'Bounty', 'Score']:
	getters[k] = partial(anongetter, k)
for k in ['Admin','Game', 'Account', 'Player', 'Session', 'Tag']:
	getters[k] = partial(owngetter, k)

@get('/apitest')
def apitest():
	return SimpleTemplate(source='<html><head> <script src="/js/prototype.js" type="text/javascript"></script><script src="/js/api.js" type="text/javascript"></script></head></html>').render()

def deref(args):
	nargs = []
	for a in args:
		i = a
		if isinstance(a, dict) and 'sqlref' in a:
			i = getters[a['sqlref']['name']](a['sqlref']['items'])
			if 'one' in a:
				i = i[0]
		nargs.append(i)
	return nargs
def derefer(func):
	def wrapped(*args, **kwargs):
		nargs = deref(args)
		nkwargs = {x:deref([kwargs[x]])[0] for x in kwargs}
		return func(*nargs, **nkwargs)
	return wrapped
class AuthException(Exception):
	pass

class API(JSONRPC):
	class Template(JSONRPC):
		@allow_auth
		def render(self, template, args):
			merged = {}
			for k in args:
				if isinstance(args[k], dict) and 'sqlref' in args[k]:
					merged[k] = getters[args[k]['sqlref']['name']](args[k]['sqlref']['items'])
					if 'one' in args[k]:
						merged[k] = merged[k][0]
			args.update(merged)
			args.update({'i18n':i18n.i18n,'lang':get_session().language,'page':template,'request': request})
			return bottle.template(template, **args)
	template = Template()
	class Database(JSONRPC):
		def get(self, klass, ids):
			print klass
			print ids
			print getters[klass]
			print getters[klass](ids)
			return list(getters[klass](ids))
	class Blog(JSONRPC):
		def posts(self):
			return list(Post.select())
		def post(self, id_):
			return Post.get(id_)
		def comments(self, post_id):
			return list(Post.get(post_id).comments)
		@allow_auth
		@derefer
		@mview('comment')
		def add_comment(self, post, content):
			user = get_session().user
			if not user:
				raise AuthException('not logged in')
			c = Comment(user=user,post=post,content=content)
			d = {'i18n':i18n.i18n,'lang':get_session().language,'page':'comment','request': request,
				 'comment': c}
			return dict(comment=c)#bottle.template('comment', **d)
	blog = Blog()
	def resolve_sqlobjs(self, klass, ids):
		return list(getters[klass](ids))
	database = Database()
	@mview('login_header')
	def login(self, user, passw):
		ac = valid_creds(user, passw)
		if not ac:
			return False
		get_session().user = ac
		allow_auth(lambda: None)()
		return dict()
	@property
	def logged_in(self):
		return get_session().user is not None
	@mview('login_header')
	def logout(self):
		get_session().destroySelf()
		allow_auth(lambda: None)()
		return dict()

build_routes(API(), lambda:get_session().skey)