from decorators import *
from database import *
from skilltester import SkillTestingQuestion
from controller import error, seterr, get_session, set_cookie
import i18n, datetime, simplejson, smtplib
from email.mime.text import MIMEText
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
	request.session['question'] = SkillTestingQuestion().as_dict
	return dict(SkillTestingQuestion=SkillTestingQuestion)
@route('/register',method='POST')
@allow_auth
@require_cond(reg_cond)
def do_registration():
	p = request.params
	data = dict([(x, request.params[x]) for x in request.params.keys()])
	del data['password_confirm']
	# must rescue the question before it becomes obliterated by field-saving code
	question = SkillTestingQuestion(request.session['question'])
	request.session.data = simplejson.dumps(data)
	for i in ['username', 'name', 'password', 'password_confirm', 'language', 'student_num', 'email', 'answer']:
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
	answer = p['answer']
	if not question.check(answer):
		seterr('/register','badanswer')
	user = (Account.from_username(username) or Player.from_student_num(studentn) or Account.from_email(email) or
			Player.from_twitter(twitter) or Player.from_cell(cell))
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
	# only obliterate the form data when player is successfully created
	request.session.data = None
	redirect('/thanks',303)

# end of non-auth pages
@route('/thanks')
@mview('thanks')
@allow_auth
@lang
@require_auth
def view_thanks():
	return dict()

@route('/forgot_password',method='GET')
@mview('forgotpass')
@allow_auth
@lang
def view_forgot_password():
	return dict()

@route('/forgot_password',method='POST')
@allow_auth
def do_forgot_password():
	email = request.params.get('email',None)
	if not email:
		seterr('/forgot_password', 'noemail')
	u = Account.from_email(email)
	if not u:
		seterr('/forgot_password', 'nouser')
	p = PasswordReset()
	p.ttl = 24*60*60	# 24 hours
	p.update_expires()
	p.user = u
	msg = MIMEText(i18n.i18n[get_session().language]['passemail']['body'] % p.skey)
	msg['Subject'] = i18n.i18n[get_session().language]['passemail']['subject']
	msg['From'] = 'passwordreset@hvsi.ca'
	s = smtplib.SMTP_SSL(Game.email_host, 465)
	s.login(Game.email_user,Game.email_pass)
	s.sendmail(msg['From'], [u.email], msg.as_string())
	redirect('/forgot_password?result=success')

@route('/stats')
@mview('graph')
@allow_auth
@lang
def view_graph():
	if not Game.is_started:
		redirect('/index', 303)
	return dict()