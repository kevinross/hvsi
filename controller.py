from bottle import view, route, run, request, response, redirect, static_file as send_file, template
import bottle, os, urllib, error_page, ops, i18n, datetime, random, string
from database import *
from ops import *
from sqlobject import *
import smtplib, database
from email.mime.text import MIMEText
iv = '6543209487240596'
key = 'd74Kv9duE8bk3Jh2'
static_root = os.getcwd()
if '_debug' in static_root:
	bottle.debug(True)
bottle.ERROR_PAGE_TEMPLATE = error_page.ERROR_PAGE_TEMPLATE
def valid_creds(user, passw):
	u = User.from_username(user)
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
def logged_in():
	return hasattr(request, 'user')
###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
css_root = os.path.join(static_root, 'css')
img_root = os.path.join(static_root, 'img')
js_root  = os.path.join(static_root, 'js')
pdf_root =os.path.join(static_root, 'pdf')
@route('/css/:file#.*#')
def static_css(file):
	return send_file(file, root=css_root)
@route('/img/:file#.*#')
def static_img(file):
	return send_file(file, root=img_root)
@route('/wmd/images/:file')
def static_wmd_img(file):
	return send_file(file, root=img_root)
@route('/images/:file#.*#')
def static_img_2(file):
	return send_file(file, root=img_root)
@route('/js/:file#.*#')
def static_js(file):
	return send_file(file, root=js_root)
@route('/wmd/images/:file')
def static_wmd(file):
	return send_file(file, root=css_root + '/images/')

@route('/pdf/:file')
def static_pdf(file):
	return send_file(file, root=pdf_root)

@route('/eula/:file')
@allow_auth
def eula_file(file):
#	response.set_cookie(file.replace('.pdf','') + '_read', 'true',path='/')
#	data = (None if 'lang' not in request.COOKIES else request.COOKIES['lang']) or (None if not (hasattr(request, 'user') and request.user) else request.user.language)
#	if not data:
#		redirect('/pdf/' + file, 303)
#	else:
#		redirect('/pdf/' + file.replace('.pdf','_' + data + '.pdf'), 303)
	from imports import static
	redirect(static('/pdf/%s' % file), 303)

@route('/index')
@mview('index')
@allow_auth
@lang
def index():
	return dict(page='index',error=None,post=Post.from_pid(1),posts=Post.select(Post.q.id > 5,orderBy='-id'))
@route('/')
@mview('countdown')
@lang
def countdown():
	return dict()
@route('/missions')
@mview('index')
@allow_auth
@lang
def index():
	return dict(page='missions',error=None,post=Post.from_pid(2))
@route('/party')
@mview('index')
@allow_auth
@lang
def index():
	return dict(page='party',error=None,post=Post.from_pid(3))
@route('/rules')
@mview('index')
@allow_auth
@lang
def index():
	return dict(page='rules',error=None,post=Post.from_pid(4))
@route('/blog')
@mview('blog')
@allow_auth
@lang
def blog():
	return dict(page='blog',error=None,posts=Post.select(Post.q.id > 5,orderBy='-id'))
	
@route('/game')
@mview('game')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_game():
	return dict()
@route('/game',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_game():
	Game.toggle_game()
	redirect('/game', 303)
@route('/reg',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_reg():
	Game.toggle_reg()
	redirect('/game', 303)
@route('/count',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_count():
	Game.toggle_countdown()
	redirect('/game', 303)
@route('/count_time',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_countdown():
	c_t = bottle.request.params.get('count_time', None)
	if not c_t:
		redirect('/game?error=notime', 302)
	Game.countdown_time = datetime.datetime.strptime(c_t,'%Y-%m-%d %H:%M:%S')
	redirect('/game', 303)
@route('/startend',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_startend():
	s_t = bottle.request.params.get('start_time', None)
	e_t = bottle.request.params.get('end_time', None)
	if not s_t or not e_t:
		redirect('/game?error=notime', 302)
	Game.game_start = datetime.datetime.strptime(s_t,'%Y-%m-%d %H:%M:%S')
	Game.game_end = datetime.datetime.strptime(e_t,'%Y-%m-%d %H:%M:%S')
	redirect('/game', 303)
@route('/rego',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_rego():
	r_t = bottle.request.params.get('rego', None)
	if not r_t:
		redirect('/game?error=notime', 302)
	Game.game_rego = datetime.datetime.strptime(r_t,'%Y-%m-%d %H:%M:%S')
	redirect('/game', 303)
@route('/hrsbc',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_hrsbc():
	hours = bottle.request.params.get('hrsbc', None)
	if not hours:
		redirect('/game?error=notime', 302)
	Game.hours_between_checkins = int(hours)
	redirect('/game', 303)
@route('/itemail',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_hrsbc():
	email = bottle.request.params.get('itemail', None)
	if not email:
		redirect('/game?error=noemail', 302)
	Game.it_email = email
	redirect('/game', 303)

@route('/login',method='GET')
@mview('login')
@allow_auth
@lang
def view_login():
	if request.logged_in:
		redirect('/', 302)
	if 'error' in request.params:
		return dict(page='login',error=request.params['error'])
	return dict(page='login',error=None)
@route('/login',method='POST')
def do_login():
	usern = request.params['username']
	passw = request.params['password']
	user = User.from_username(usern)
	if not user:
		redirect('/login?error=nouser', 302)
	if user.verify_pass(passw):
		sess = get_session()
		# protect against session fixation
		sess.destroySelf()
		sess = get_session()
		sess.user = user
		if isinstance(user, Station):
			sess.ttl = +(5*24*60*60)
			sess.update_expires()
		set_cookie(sess)
		response.set_header('Location', request.environ.get('HTTP_REFERER', '/index'))
		response.status = 303
	else:
		seterr('/login', 'nouser')
	return None

@route('/logout')
def do_logout():
	get_session().destroySelf()
	redirect('/')

@route('/eula', method='GET')
@mview('eula')
@allow_auth
@lang
def view_eula():
	if request.user.liability and request.user.safety:
		redirect('/', 303)
	i18n_o = i18n.override_title('eula',i18n.i18n['e']['pages']['eula']['title'],i18n.i18n['f']['pages']['eula']['title'])
	for i in ('e','f'):
		i18n_o[i]['pages']['register']['agree'] = i18n.i18n[i]['pages']['eula']['agree']
	return dict(error=request.params.get('error',None),page='register',
				i18n=i18n_o)

@route('/eula', method='POST')
@allow_auth
@require_auth
@require_role(Player)
def do_eula():
	for i in ('liability','safety'):
#		if i+'_read' not in request.COOKIES or request.COOKIES[i+'_read'] != 'true':
#			redirect('/eula?error='+i+'_read', 302)
		if i not in request.params:
			redirect('/eula?error='+i, 302)
		setattr(request.user, i, True)
	redirect('/', 303)
def reg_cond():
	if request.admin or request.station:
		return True
	if not Game.is_reg and datetime.datetime.now() < Game.game_rego:
		return False
	else:
		return datetime.datetime.now() < Game.game_rego
@route('/register',method='GET')
@mview('register')
@allow_auth
@lang
@require_cond(reg_cond)
def view_registration():
	return dict(error=request.params.get('error',None),page='register')
@route('/register',method='POST')
@allow_auth
@require_cond(reg_cond)
def do_registration():
	p = request.params
	for i in ['username', 'name', 'password', 'password_confirm', 'language', 'student_num', 'email']:
		if not p[i]:
			redirect('/register?error=missinginfo', 303)
	if '/' in p['username']:
		redirect('/register?error=noslash', 303)
	for i in ('liability', 'safety'):
#		if i+'_read' not in request.COOKIES or request.COOKIES[i+'_read'] != 'true':
#			redirect('/register?error='+i+'_read', 303)
		if i not in request.params:
			redirect('/register?error='+i+'_err', 303)
	name = p['name']
	username = p['username']
	password = p['password']
	language = p['language']
	studentn = int(p['student_num'])
	email = p['email']
	twitter = None if not p['twitter'] else p['twitter'].replace('@','')
	cell = None if not p['cell'] else p['cell']
	user = (User.from_username(username) or User.from_student_num(studentn) or User.from_email(email) or
		   User.from_twitter(twitter) or User.from_cell(cell))
	if user:
		redirect('/register?error=userexists', 303)
	u = None
	try:
		u = Player(name=name,username=username,hashed_pass=password,language=language,student_num=studentn,
			   email=email,twitter=twitter,cell=cell,liability=True,safety=True)
	except dberrors.DuplicateEntryError, e:
		redirect('/register?error=userexists', 302)
	if hasattr(request, 'station') and not request.station and not request.admin:
		sess = get_session()
		sess.user = u
		set_cookie(sess)
	redirect('/thanks',303)

# end of non-auth pages
@route('/thanks')
@mview('thanks')
@allow_auth
@lang
@require_auth
def view_thanks():
	return dict(error=None,page='thanks')
	
@route('/users')
@mview('users')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_users():
	return dict(error=request.params.get('error',None),users=Player.select(Player.q.username != 'military.militaire',orderBy=[Player.q.state,User.q.username]),page='userlist')

@route('/users',method='POST')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def find_user():
	value = request.params['value']
	cat = request.params['cat']
	try:
		p = None
		if cat == 'email':
			p = Player.from_email(value)
		elif cat == 'twitter':
			p = Player.from_twitter(value)
		elif cat == 'cell':
			p = Player.from_cell(value)
		elif cat == 'student':
			p = Player.from_student_num(int(value))
		elif cat == 'game_id':
			p = Player.from_game_id(value.upper())
	except:
		redirect('/users?error=nouser&cat=%s' % cat, 302)
	if not p:
		redirect('/users?error=nouser&cat=%s' % cat, 302)
	redirect('/user/%s' % p.username, 302)

@route('/users',method='POST')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def find_user():
	value = request.params['value']
	cat = request.params['cat']
	try:
		p = None
		if cat == 'email':
			p = Player.from_email(value)
		elif cat == 'twitter':
			p = Player.from_twitter(value)
		elif cat == 'cell':
			p = Player.from_cell(value)
		elif cat == 'student':
			p = Player.from_student_num(int(value))
		elif cat == 'game_id':
			p = Player.from_game_id(value.upper())
	except:
		redirect('/users?error=nouser&cat=%s' % cat, 302)
	redirect('/user/%s' % p.username, 302)

@route('/user/:name')
@mview('user_view')
@allow_auth
@lang
@require_auth
def view_user(name):
	if request.station and not ('HTTP_REFERER' in request.environ and '/station' in request.environ['HTTP_REFERER']):
		error(code=401)
	if (not request.admin) and (request.user.username != name) and not request.station:
		error(code=401)
	user = User.get_user(name)
	if not user:
		error(code=404)
	return dict(error=None,vuser=user,page='user',i18n=i18n.override_title('user',user.username,user.username))

@route('/user/:name/edit',method='GET')
@mview('user_edit')
@allow_auth
@lang
@require_auth
@require_role(Admin,Player)
def view_user_edit(name):
	if not request.admin and request.user.username != name:
		error(code=401)
	user = User.get_user(name)
	if not user:
		error(code=404)
	return dict(error=request.params.get('error',None),page='useredit',vuser=user,
				i18n=i18n.override_title('useredit',
										 i18n.i18n['e']['pages']['useredit']['editing'] + ' ' + user.username,
										 i18n.i18n['f']['pages']['useredit']['editing'] + ' ' + user.username))

@route('/user/:name/edit',method='POST')
@allow_auth
@require_auth
@require_role(Admin,Player)
def do_user_edit(name):
	if not request.admin and request.user.username != name:
		error(code=401)
	p = request.params
	user = User.get_user(name)
	# whitelist the paras a player may pass in
	perm_user = ['verify_password','password','confirm_password','language','cell','twitter','email']
	if request.player:
		# filter the params down to the permitted ones
		p = dict([(x,p[x]) for x in perm_user if x in p])
	if 'password' in p and p['password'] and not request.admin:
		if p['password'] != p['confirm_password']:
			redirect('/user/' + name + '/edit?error=vp')
		if not user.verify_pass(p['verify_password']):
			redirect('/user/' + name + '/edit?error=bp')
	for prop in ['language','cell','twitter','name','username','state','signedin','student_num','email']:
		if prop in p:
			if p[prop]:
				try:
					i = int(p[prop])
					setattr(user,prop,int(p[prop]))
				except:
					setattr(user,prop,p[prop])
			else:
				setattr(user,prop,None)
	if p['password']:
		user.hashed_pass = p['password']
	redirect('/user/' + name, 303)
@route('/user/:name/zero',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_user_zero(name):
	user = User.get_user(name)
	if not user:
		error(code=404)
	user.zero = True
	redirect(request.environ.get('HTTP_REFERER','/'), 303)
@route('/user/:name/activate',method='POST')
@allow_auth
@require_auth
@require_role(Admin,Station)
def do_user_activate(name):
	# 'liability', 'safety', 'kitted'
	u = User.get_user(name)
	if not u:
		redirect('/station?section=activate&err=noplayer', 303)
	for i in ('liability', 'safety', 'signedin'):
		setattr(u, i, getattr(u, i) or 'kitted' in request.params)
	u.signedin_time = datetime.datetime.now()
	Checkin(location=request.user.location,player=u)
	if request.logged_in and request.admin:
		redirect(request.environ['HTTP_REFERER'], 303)
	redirect('/station', 303)
@route('/user/:name/tags',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_user_tags(name):
	user = User.get_user(name)
	if not user:
		error(code=404)
	if 'username' not in request.params:
		redirect('/station?error=noplayer', 302)
	redirect('/'.join(['/tag',name,request.params['username']]), 302)

@route('/user/:name/checkins',method='GET')
@mview('checkins')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def get_user_checkins(name):
	user = User.get_user(name)
	if not user:
		error(code=404)
	return dict(error=request.params.get('error',None),page='checkins',vuser=user,checkins=user.checkins.orderBy(Checkin.q.time))
@route('/user/:name/checkins/add',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def add_user_checkin(name):
	user = User.get_user(name)
	if not user:
		error(code=404)
	# no location or time
	if not 'location' in request.params:
		redirect('/user/%s/checkins?error=noloc' % user.username, 302)
	if not 'time' in request.params:
		redirect('/user/%s/checkins?error=notime' % user.username, 302)
	# bad location
	if not request.params['location'] in database.locations:
		redirect('/user/%s/checkins?error=badloc' % user.username, 302)
	# bad time
	time = None
	try:
		time = datetime.datetime.strptime(request.params['time'],'%Y-%m-%d %H:%M:%S')
	except:
		redirect('/user/%s/checkins?error=badtime' % user.username, 302)
	location = request.params['location']
	Checkin(time=time,location=location,player=user)
	redirect('/user/%s/checkins' % name, 303)
@route('/user/:name/checkins/delete',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def del_user_checkins(name):
	user = User.get_user(name)
	if not user:
		error(code=404)
	# checkins are like checkin_[id]
	ids = [int(x[x.find('_')+1:]) for x in request.params if 'checkin_' in x]
	_ = [Checkin.select(Checkin.q.id == x)[0].destroySelf() for x in ids]
	redirect('/user/%s/checkins' % user.username, 303)
@route('/password_reset',method='GET')
@mview('pass_reset')
@allow_auth
@lang
def view_pass_reset():
	i18n_reg_e = i18n.i18n_over({'nonsensical':'bullshit'})['e']['pages']['register']
	del i18n_reg_e['title']
	i18n_reg_f = i18n.i18n_over({'nonsensical':'bullshit'})['f']['pages']['register']
	del i18n_reg_f['title']
	if 'success' in request.params:
		redirect('/', 302)
	return dict(error=request.params.get('error',None),page='pass_reset',
				i18n=i18n.i18n_over({'e':{'pages':{'pass_reset':i18n_reg_e}},
									 'f':{'pages':{'pass_reset':i18n_reg_f}}}))
@route('/password_reset',method='POST')
def do_pass_reset():
	for i in ('email', 'student_num'):
		if i not in request.params:
			redirect('/password_reset?error=missinginfo', code=302)
	user = User.get_user(request.params['email'])
	if not user:
		redirect('/password_reset?error=wronginfo', code=302)
	if user.student_num != int(request.params['student_num']):
		redirect('/password_reset?error=wronginfo', code=302)
	user.hashed_pass = str(user.student_num)
	redirect('/password_reset?success=true', 303)
@route('/tag',method='GET')
@mview('tag')
@allow_auth
@lang
@require_auth
def view_tag():
	return dict(error=request.params.get('error',None),page='tag',
				# copy station errors to tag
				i18n=i18n.i18n_over({'e':{'pages':{'tag':i18n.i18n['e']['pages']['station']['errors']}},
									 'f':{'pages':{'tag':i18n.i18n['f']['pages']['station']['errors']}}}
				))
@route('/tag',method='POST')
@allow_auth
@require_auth
def do_tag():
	if 'taggee' not in request.params:
		redirect('/tag?error=badinput', 302)
	if 'uid' not in request.params:
		redirect('/tag?error=badinput', 302)
	if not Game.is_started:
		redirect('/tag?error=game', 302)
	error = None
	try:
		kill = add_kill(request.user, request.params['taggee'], request.params['uid'])
	except TagException, e:
		if e.message == ops.EXC_NOTHUMAN:
			error = 'nothuman'
		elif e.message == ops.EXC_NOTZOMBIE:
			error = 'notzombie'
		elif e.message == ops.EXC_KITHUMAN:
			error = 'kithuman'
		elif e.message == ops.EXC_KITZOMBIE:
			error = 'kitzombie'
		elif e.message == ops.EXC_CHEATER:
			error = 'duplicate'
		else:
			error = 'unknown'
	if error:
		redirect('/tag?error=' + error, 302)
	else:
		if 'HTTP_REFERER' in request.environ:
			pg = request.environ['HTTP_REFERER']
			if 'error' in pg:
				pg = pg[::-1]
				pg = pg[pg.find('?')+1][::-1]
			redirect(pg, 302)
		else:
			redirect('/', 302)
@route('/tags', method='GET')
@mview('tags')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_all_tags():
	return dict(page='tags', error=request.params.get('error',None),
				tags = Tag.select(orderBy=Tag.q.time))
@route('/tag/:tagger', method='GET')
@mview('tags')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_tags(tagger):
	tagger = User.get_user(tagger)
	if not tagger:
		error(code=404)
	return dict(page='tags', error=request.params.get('error',None),
				tagger=tagger,
				tags=Tag.select(OR(Tag.q.tagger == tagger,Tag.q.taggee == tagger),orderBy=Tag.q.time))
@route('/tag/:tagger/:taggee', method='GET')
@mview('tags')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_tags(tagger, taggee):
	tagger = User.get_user(tagger)
	taggee = User.get_user(taggee)
	if not tagger or not taggee:
		error(code=404)
	return dict(page='tags', error=request.params.get('error',None),
				tagger=tagger,
				taggee=taggee,
				tags=Tag.select(OR(
									AND(Tag.q.tagger == tagger, Tag.q.taggee == taggee),
									AND(Tag.q.tagger == taggee, Tag.q.taggee == tagger)
								)))
@route('/tagrm', method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_tags_rm():
	# get the removals
	raw_text = [(x[2:],False) for x in request.params.keys() if x[0:2] == 'rm']
	# get the zombies to cure
	raw_text = [(x[0].split('/'),('cu' + x[0]) in request.params) for x in raw_text]
	# raw_text = [[time, tagger, taggee], ...]
	raw_vals = [(datetime.datetime.strptime(x[0][0],"%Y-%m-%dT%H:%M:%S"), User.get_user(x[0][1]), User.get_user(x[0][2]),x[1]) for x in raw_text]
	tags = [(Tag.select(Tag.q.time == x[0] and Tag.q.tagger == x[1] and Tag.q.taggee == x[2]),x[3]) for x in raw_vals]
	tags = [(x[0][0],x[1]) for x in tags if x[0].count() > 0]
	for tag in tags:
		taggee = tag[0].taggee
		tag[0].destroySelf()
		if tag[1]:
			taggee.cure()
	redirect('/station' if 'HTTP_REFERER' not in request.environ else request.environ['HTTP_REFERER'], 302)
@route('/webcheckin')
@mview('webcheckin')
@allow_auth
@lang
@require_auth
@require_role(Player)
def view_webcheckin():
	return dict(page='webcheckin',error=request.params.get('error',None))
@route('/webcheckin',method='POST')
@allow_auth
@require_auth
@require_role(Player)
def do_webcheckin():
	p = request.params
	if 'confirm' not in p:
		redirect('/webcheckin?error=notconfirmed', 302)
	if request.user.did_webcheckin:
		redirect('/webcheckin?error=alreadyused', 302)
	station = User.get_user('zombie_internet')
	if not station:
		redirect('/webcheckin?error=code499', 302)
	try:
		do_checkin(request.user, station)
	except CheckInException, e:
		err = e.message[::-1]
		err = err[:err.find(' ')][::-1]
		redirect('/webcheckin?error=' + err, 302)
	redirect('/', 302)
@route('/post/view/:pid')
@mview('index')
@allow_auth
@lang
def view_post(pid):
	try:
		p = Post.from_pid(pid)
		return dict(error=None,post=p,page='index',i18n=i18n.override_title('index',p.title_e,p.title_f))
	except:
		error(code=404)
@route('/post/view/:pid/comment',method='POST')
@allow_auth
@lang
@require_auth
def do_comment(pid):
	p = request.params
	try:
		po = Post.from_pid(pid)
	except:
		error(code=404)
	if not p['comment']:
		redirect('/post/view/' + str(pid) + '?error=nocontent', 302)
	if Comment.select(Comment.q.user == request.user and Comment.q.content == p['comment']).count() > 0:
		redirect('/post/view/' + str(pid) + '?error=exists', 302)
	c = Comment(user=request.user, content=p['comment'], post=po)
	redirect('/post/view/' + str(pid) + '#comment-' + str(c.id), 302)
@route('/post/create',method='GET')
@mview('create_editpost')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def create_post():
	return dict(error=None,mode='create',page='post_create')

@route('/post/create',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def create_post_post():
	p = request.params
	# content_e, content_f, title_e, title_f
	if not p['content_e'] or not p['content_f'] or not p['title_e'] or not p['title_f']:
		redirect('/post/create?error=missinginfo', 302)
	if p['content_e_hidden']:
		p['content_e'] = p['content_e_hidden']
	if p['content_f_hidden']:
		p['content_f'] = p['content_f_hidden']
	if 'allow_comments' in p:
		p['allow_comments'] = True
	else:
		p['allow_comments'] = False
	p = dict([(x,p[x]) for x in ['content_e','content_f','title_e','title_f','allow_comments']])
	post = Post(**p)
	redirect('/post/view/' + str(post.id),303)
	
@route('/post/edit/:pid',method='GET')
@mview('create_editpost')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_edit_post(pid):
	try:
		p = Post.from_pid(pid)
		return dict(error=None,post=p,mode='edit',page='post_edit',
					i18n=i18n.override_title('post_edit','Editing EN:"' + p.title_e + '" FR:"' + p.title_f + '"','Editing "' + p.title_f + '"'))
	except IndexError, e:
		return dict(error='nopostpid',mode='edit')
	except:
		return dict(error='unknown',mode='edit')
@route('/post/edit/:pid',method='POST')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def do_edit_post(pid):
	p = request.params
	try:
		post=Post.from_pid(pid)
	except IndexError, e:
		redirect(request.path+'?error=nopostpid', 302)
	except:
		redirect(request.path+'?error=unknown', 302)
	if p['content_e_hidden']:
		p['content_e'] = p['content_e_hidden']
	if p['content_f_hidden']:
		p['content_f'] = p['content_f_hidden']
	if 'allow_comments' in p:
		p['allow_comments'] = True
	else:
		p['allow_comments'] = False
	p = dict([(x,p[x]) for x in ['content_e','content_f','title_e','title_f','allow_comments']])
	p['time'] = datetime.datetime.now()
	for i in p:
		setattr(post, i, p[i])
	redirect('/post/view/' + str(pid), 303)
@route('/post/delete/:pid')
@allow_auth
@require_auth
@require_role(Admin)
def delete_post(pid):
	try:
		p = Post.from_pid(pid)
	except IndexError, e:
		return
	p.delete()
	redirect('/', 303)


@route('/station')
@mview('station')
@allow_auth
@lang
@require_auth
@require_role(Admin, Station)
def view_stationops():
	if 'section' in request.params:
		return dict(error='generic',section=request.params['section'],err=request.params['err'],page='station',post=Post.from_pid(5))
	return dict(error=None,page='station',post=Post.from_pid(5))
@route('/station/checkin', method='POST')
@allow_auth
@require_auth
@require_role(Admin,Station)
def do_station_checkin():
	if 'user_id' not in request.params:
		redirect('/station?section=checkin&err=nouid', 303)
	try:
		do_checkin(request.params['user_id'], request.user)
	except CheckInException, e:
		if e.message == ops.EXC_NOTHUMAN:
			redirect('/station?section=checkin&err=nothuman', 303)
		elif e.message == ops.EXC_KITHUMAN:
			redirect('/station?section=checkin&err=kithuman', 303)
		elif e.message == ops.CHECKIN_TOOSOON:
			redirect('/station?section=checkin&err=toosoon', 303)
		elif e.message == ops.EXC_NOTSTATION:
			redirect('/station?section=checkin&err=wtf', 303)
		elif e.message == ops.EXC_NOSUCHHUMAN:
			redirect('/station?section=checkin&err=nohuman', 303)
		else:
			redirect('/station?section=checkin&err=unknown', 303)
	except:
		redirect('/station?section=checkin&err=unknown', 303)
	redirect('/station', code=303)

@route('/station/activate', method='POST')
@allow_auth
@require_auth
@require_role(Admin,Station)
def do_station_activate():
	if 'user_id' not in request.params:
		redirect('/station?section=activate&err=nuid', 303)
	try:
		i = int(request.params['user_id'])
	except:
		redirect('/station?section=activate&err=nuid', 303)
	user = User.from_student_num(int(request.params['user_id']))
	if not user:
		redirect('/station?section=activate&err=noplayer', 303)
	if user.signedin:
		redirect('/station?section=activate&err=activated', 303)
	redirect('/user/' + user.username, 303)
@route('/station/cure', method='POST')
@allow_auth
@require_auth
@require_role(Admin,Station)
def do_station_cure():
	if 'user_id' not in request.params:
		redirect('/station?section=cure&err=nouid', 303)
	if 'cure_id' not in request.params:
		redirect('/station?section=cure&err=nocid', 303)
	try:
		do_cure(request.params['user_id'], request.user, request.params['cure_id'])
	except CureException, e:
		if e.message == ops.EXC_NOTZOMBIE:
			redirect('/station?section=cure&err=notzombie', 303)
		elif e.message == ops.EXC_KITZOMBIE:
			redirect('/station?section=cure&err=kitzombie', 303)
		elif e.message == ops.EXC_NOTSTATION:
			redirect('/station?section=cure&err=wtf', 303)
		elif e.message == ops.CURE_DISQUALIFIED:
			redirect('/station?section=cure&err=disq', 303)
		elif e.message == ops.CURE_ALREADYUSED:
			redirect('/station?section=cure&err=used', 303)
		elif e.message == ops.CURE_EXPIRED:
			redirect('/station?section=cure&err=exp', 303)
		elif e.message == ops.EXC_NOSUCHZOMBIE:
			redirect('/station?section=checkin&err=nozombie', 303)
		else:
			redirect('/station?section=cure&err=unknown', 303)
	except:
		redirect('/station?section=cure&err=unknown', 303)
	redirect('/station', code=303)
@route('/station/tag', method='POST')
@allow_auth
@require_auth
@require_role(Admin,Station)
def do_station_tag():
	if 'tagger_id' not in request.params:
		redirect('/station?section=kill&err=notzombie', 303)
	if 'taggee_id' not in request.params:
		redirect('/station?section=kill&err=nothuman', 303)
	if not Game.is_started:
		redirect('/station?error=game', 303)
	try:
		uid = request.user.username + '_' + ''.join(random.sample(string.ascii_letters+string.digits, 36))
		add_kill(request.params['tagger_id'],request.params['taggee_id'].upper(), uid)
	except TagException, e:
		if e.message == ops.EXC_NOTHUMAN:
			redirect('/station?section=kill&err=nothuman', 303)
		elif e.message == ops.EXC_NOTZOMBIE:
			redirect('/station?section=kill&err=notzombie', 303)
		elif e.message == ops.EXC_KITHUMAN:
			redirect('/station?section=kill&err=kithuman', 303)
		elif e.message == ops.EXC_KITZOMBIE:
			redirect('/station?section=kill&err=kitzombie', 303)
		elif e.message == ops.EXC_NOSUCHHUMAN:
			redirect('/station?section=kill&err=nohuman', 303)
		elif e.message == ops.EXC_NOSUCHZOMBIE:
			redirect('/station?section=kill&err=nozombie', 303)
		elif e.message == ops.EXC_CHEATER:
			redirect('/station?section=kill&err=duplicate', 303)
		else:
			redirect('/station?section=kill&err=unknown', 303)
	redirect('/station', code=303)

@route('/cures')
@mview('cures')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_cures():
	return dict(page='cures',error=None,cures=Cure.select())

@route('/cures/edit/:cid',method='GET')
@mview('cure_edit')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_edit_cure(cid):
	try:
		c = Cure.get_cure(int(cid))
	except:
		c = Cure.get_cure(cid)
	if not c:
		error(code=404)
	return dict(error=None,page='editcure',cure=c)
@route('/cures/edit/:cid',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_edit_cure(cid):
	try:
		c = Cure.get_cure(int(cid))
	except:
		c = Cure.get_cure(cid)
	# time, used, username, disqualified
	time = request.params.get('time',None)
	expiry = request.params.get('expiry',None)
	username = request.params.get('username',None)
	time = None if not request.params['time'] else request.params['time']
	username = None if not request.params['username'] else request.params['username']
	used = 'used' in request.params
	disqualified = 'disqualified' in request.params
	if time:
		c.time = datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%S")
	if expiry:
		c.expiry = datetime.datetime.strptime(expiry,"%Y-%m-%dT%H:%M:%S")
	if username:
		c.player = User.get_user(username)
	if c.player:
		used = True
		c.player.cure()
	c.used = used
	c.disqualified = disqualified
	redirect(request.path, 303)
@route('/cures/add', method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_add_cure():
	Cure()
	redirect('/cures', 303)
@route('/cures/massdelete', method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_mass_rm_cure():
	if not request.params.keys():
		redirect('/cures', 303)
	cure_ids = [int(x.replace('cure_','')) for x in request.params.keys()]
	cures = [Cure.get_cure(x) for x in cure_ids]
	cures = [x for x in cures if x]
	for cure in cures:
		if cure.used:
			cure.player.kill()
		cure.destroySelf()
	redirect('/cures', 303)
@route('/stats')
@mview('graph')
@allow_auth
@lang
def graph():
	if not Game.is_started:
		redirect('/index', 302)
	return dict(error=None,page='stats')
@route('/email', method='GET')
@mview('email')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_shotgun_email():
	return dict(error=(None if 'error' not in request.params else request.params['error']), page='email')
@route('/email', method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_shotgun_email():
	s = smtplib.SMTP_SSL('localhost',465)
	s.login('hvsi@hvsi.ca','HvsI_email_sender')
	if 'msg' not in request.params:
		redirect('/email?error=nomsg', 302)
	msg = MIMEText(request.params['msg'])
	if 'subject' not in request.params:
		redirect('/email?error=nosubj', 302)
	msg['Subject'] = request.params['subject']
	if 'from' not in request.params:
		redirect('/email?error=nofrom', 302)
	msg['From'] = request.params['from']
	if request.params['target'] == 'humans':
		to = [x.email for x in Player.humans]
	elif request.params['target'] == 'zombies':
		to = [x.email for x in Player.zombies]
	elif request.params['target'] == 'active':
		to = [x.email for x in Player.users]
	elif request.params['target'] == 'inactive':
		to = [x.email for x in Player.select(Player.q.signedin == False).filter(Player.q.username != 'military.militaire')]
	elif request.params['target'] == 'all':
		to = [x.email for x in Player.select(Player.q.username != 'military.militaire')]
	s.sendmail(msg['From'], ['president@hvsi.ca'] + to, msg.as_string())
	redirect('/', 303)
# catch all perm-redirect
@route('/:page#.+#/')
def redir(page):
	redirect('/' + page, 301)
