from decorators import *
from database import *
from controller import error, seterr, get_session, set_cookie
import i18n, datetime, simplejson
from bottle import route, request, response, redirect
from sqlobject import dberrors
@route('/index')
@mview('index')
@allow_auth
@lang
def view_index():
	return dict(post=Post.from_pid(1),posts=Post.select(Post.q.id > 5,orderBy='-id'))
@route('/')
@mview('countdown')
@lang
def view_countdown():
	return dict()
@route('/missions')
@mview('index')
@allow_auth
@lang
def view_missions():
	return dict(page='missions',post=Post.from_pid(2))
@route('/party')
@mview('index')
@allow_auth
@lang
def view_party():
	return dict(page='party',post=Post.from_pid(3))
@route('/rules')
@mview('index')
@allow_auth
@lang
def view_rules():
	return dict(page='rules',post=Post.from_pid(4))
@route('/blog')
@mview('blog')
@allow_auth
@lang
def view_blog():
	return dict(posts=Post.select(Post.q.id > 5,orderBy='-id'))
@route('/login',method='GET')
@mview('login')
@allow_auth
@lang
def view_login():
	if request.logged_in:
		redirect('/index', 303)
	return dict()
@route('/login',method='POST')
def do_login():
	usern = request.params['username']
	passw = request.params['password']
	user = Account.from_username(usern)
	if not user:
		seterr('/login','nouser')
	if not user.verify_pass(passw):
		seterr('/login','nouser')
	sess = get_session()
	# protect against session fixation
	sess.destroySelf()
	sess = get_session()
	sess.user = user
	if isinstance(user, Station):
		sess.ttl = +(5*24*60*60)
		sess.update_expires()
	set_cookie(sess)
	loc = request.environ.get('HTTP_REFERER', '/index')
	if loc == '/':
		loc = '/index'
	response.set_header('Location', loc)
	response.status = 303
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
	return dict(page='register',
				i18n=i18n_o)

@route('/eula', method='POST')
@allow_auth
@require_auth
@require_role(Player)
def do_eula():
	for i in ('liability','safety'):
	#		if i+'_read' not in request.COOKIES or request.COOKIES[i+'_read'] != 'true':
	#			redirect('/eula?error='+i+'_read', 303)
		if i not in request.params:
			seterr('/eula', i)
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
	return dict()
@route('/register',method='POST')
@allow_auth
@require_cond(reg_cond)
def do_registration():
	p = request.params
	data = dict([(x, request.params[x]) for x in request.params.keys()])
	del data['password_confirm']
	request.session.data = simplejson.dumps(data)
	for i in ['username', 'name', 'password', 'password_confirm', 'language', 'student_num', 'email']:
		if not p[i]:
			seterr('/register','missinginfo')
	if '/' in p['username']:
		seterr('/register','noslash')
	for i in ('liability', 'safety'):
	#		if i+'_read' not in request.COOKIES or request.COOKIES[i+'_read'] != 'true':
	#			redirect('/register?error='+i+'_read', 303)
		if i not in request.params:
			seterr('/register',i+'_err')
	name = p['name']
	username = p['username']
	password = p['password']
	language = p['language']
	studentn = int(p['student_num'])
	email = p['email']
	twitter = None if not p['twitter'] else p['twitter'].replace('@','')
	cell = p.get('cell', None)
	user = (Account.from_username(username) or Account.from_student_num(studentn) or Account.from_email(email) or
			Account.from_twitter(twitter) or Account.from_cell(cell))
	if user:
		seterr('/register','userexists')
	u = None
	try:
		u = Player(name=name,username=username,hashed_pass=password,language=language,student_num=studentn,
				   email=email,twitter=twitter,cell=cell,liability=True,safety=True)
	except dberrors.DuplicateEntryError, e:
		seterr('/register', 'userexists')
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
	return dict()
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
		redirect('/', 303)
	return dict(i18n=i18n.i18n_over({'e':{'pages':{'pass_reset':i18n_reg_e}},
									 'f':{'pages':{'pass_reset':i18n_reg_f}}}))
@route('/password_reset',method='POST')
def do_pass_reset():
	for i in ('email', 'student_num'):
		if i not in request.params:
			seterr('/password_reset', 'missinginfo')
	user = Account.get_user(request.params['email'])
	if not user:
		seterr('/password_reset', 'wronginfo')
	if user.student_num != int(request.params['student_num']):
		seterr('/password_reset', 'wronginfo')
	user.hashed_pass = str(user.student_num)
	redirect('/password_reset?success=true', 303)
@route('/stats')
@mview('graph')
@allow_auth
@lang
def view_graph():
	if not Game.is_started:
		redirect('/index', 303)
	return dict()