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
	database = Database()
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
	class Game(JSONRPC):
		@property
		def is_countdown(self):
			return Game.is_countdown
		@property
		def countdown_time(self):
			return Game.countdown_time
		@property
		def start_time(self):
			return Game.game_start
		@property
		def end_time(self):
			return Game.game_end
		@property
		def can_register(self):
			return Game.is_reg
		@property
		def support_email(self):
			return Game.it_email
	game = Game()
	def get_string(self, path):
		s = get_session()
		lang = s.language if not s.user else s.user.language
		parts = path.split('/')
		base = i18n.i18n[lang]
		for part in parts:
			base = base[part]
		return base
	def login(self, user, passw):
		ac = valid_creds(user, passw)
		if not ac:
			return False
		get_session().user = ac
		allow_auth(lambda: None)()
		return True
	@property
	def logged_in(self):
		return get_session().user is not None
	def logout(self):
		get_session().destroySelf()
		allow_auth(lambda: None)()
		return True
	def forgot_password(self, username):
		try:
			user = Account.from_username(username)
			return True
		except:
			return False
	@property
	def self(self):
		return get_session().user
	@property
	def language(self):
		s = get_session()
		return s.language if not s.user else s.user.language

	def register(self, *vals):
		tmap = ['email','hashed_pass','pass_confirm','username','name','student_num','twitter','cell','language']
		params = {tmap[x]:vals[x] for x in range(0, len(tmap) - 1) if vals[x] != ''}
		if params['hashed_pass'] != params['pass_confirm']:
			return dict(result='false',message='pass')
		del params['pass_confirm']
		params['student_num'] = int(params['student_num'])
		user = (Account.from_username(params['username']) or Player.from_student_num(params['student_num']) or Account.from_email(params['email']) or
			Player.from_twitter(params['twitter']) or Player.from_cell(params['cell']))
		if user:
			return dict(result='false',message='dup')
		try:
			u = Player(**params)
			get_session().user = u
			return dict(result='true',message=str(u.id))
		except dberrors.DuplicateEntryError, e:
			return dict(result='false',message='dup')
		except Exception, e:
			return dict(result='false',message=str(e))



build_routes(API(), lambda:get_session().skey)