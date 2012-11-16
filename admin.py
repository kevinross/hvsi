from decorators import *
from database import *
from controller import error, seterr
import bottle, datetime, simplejson, smtplib
from email.mime.text import MIMEText
from bottle import route, redirect, request
from sqlobject import OR, AND
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
		seterr('/game', 'notime')
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
		seterr('/game', 'notime')
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
		seterr('/game', 'notime')
	Game.game_rego = datetime.datetime.strptime(r_t,'%Y-%m-%d %H:%M:%S')
	redirect('/game', 303)
@route('/hrsbc',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_hrsbc():
	hours = bottle.request.params.get('hrsbc', None)
	if not hours:
		seterr('/game', 'notime')
	Game.hours_between_checkins = int(hours)
	redirect('/game', 303)
@route('/itemail',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_itemail():
	email = bottle.request.params.get('itemail', None)
	if not email:
		seterr('/game', 'noemail')
	Game.it_email = email
	redirect('/game', 303)


@route('/users')
@mview('users')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_users():
	return dict(users=
	Player.select(
		Player.q.username != 'military.militaire',
		orderBy=[Player.q.state,Account.q.username]))

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
		seterr('/users?cat=%s' % cat, 'nouser')
	if not p:
		seterr('/users?cat=%s' % cat, 'nouser')
	redirect('/user/%s' % p.username, 303)

@route('/users',method='POST')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def do_find_user():
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
		seterr('/users?cat=%s' % cat, 'nouser')
	redirect('/user/%s' % p.username, 303)

@route('/tags', method='GET')
@mview('tags')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_all_tags():
	return dict(tags=Tag.select(orderBy=Tag.q.time))
@route('/tag/:tagger', method='GET')
@mview('tags')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_tags(tagger):
	tagger = Account.get_user(tagger)
	if not tagger:
		error(code=404)
	return dict(tagger=tagger,
				tags=Tag.select(OR(Tag.q.tagger == tagger,Tag.q.taggee == tagger),orderBy=Tag.q.time))
@route('/tag/:tagger/:taggee', method='GET')
@mview('tags')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_tags(tagger, taggee):
	tagger = Account.get_user(tagger)
	taggee = Account.get_user(taggee)
	if not tagger or not taggee:
		error(code=404)
	return dict(tagger=tagger,
				taggee=taggee,
				tags=Tag.select(OR(
					AND(Tag.q.tagger == tagger, Tag.q.taggee == taggee),
					AND(Tag.q.tagger == taggee, Tag.q.taggee == tagger)
				)))
@route('/tagrm', method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_del_tags():
	# get the removals
	raw_text = [(x[2:],False) for x in request.params.keys() if x[0:2] == 'rm']
	# get the zombies to cure
	raw_text = [(x[0].split('/'),('cu' + x[0]) in request.params) for x in raw_text]
	# raw_text = [[time, tagger, taggee], ...]
	raw_vals = [(datetime.datetime.strptime(x[0][0],"%Y-%m-%dT%H:%M:%S"), Account.get_user(x[0][1]), Account.get_user(x[0][2]),x[1]) for x in raw_text]
	tags = [(Tag.select(Tag.q.time == x[0] and Tag.q.tagger == x[1] and Tag.q.taggee == x[2]),x[3]) for x in raw_vals]
	tags = [(x[0][0],x[1]) for x in tags if x[0].count() > 0]
	for tag in tags:
		taggee = tag[0].taggee
		tag[0].destroySelf()
		if tag[1]:
			taggee.cure()
	redirect(request.environ.get('HTTP_REFERER','/station'), 303)
@route('/cures')
@mview('cures')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_cures():
	return dict(cures=Cure.select())

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
	return dict(cure=c)
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
		c.player = Account.get_user(username)
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
def do_del_cure():
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
@route('/email', method='GET')
@mview('email')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_shotgun_email():
	return dict()
@route('/email', method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_shotgun_email():
	request.session.data = simplejson.dumps(dict([(x, request.params[x]) for x in request.params.keys()]))
	msg = request.params.get('msg', None)
	subject = request.params.get('subject', None)
	from_ = request.params.get('from', None)
	if msg == '' or msg is None:
		seterr('/email', 'nomsg')
	msg = MIMEText(msg)
	if subject == '' or subject is None:
		seterr('/email', 'nosubj')
	msg['Subject'] = subject
	if from_ == '' or from_ is None:
		seterr('/email', 'nofrom')
	msg['From'] = from_
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
	s = None
	try:
		s = smtplib.SMTP_SSL(Game.email_host,465)
	except:
		seterr('/email', 'nocon')
	try:
		s.login(Game.email_user,Game.email_pass)
	except:
		seterr('/email', 'badlogin')
	try:
		s.sendmail(msg['From'], ['president@hvsi.ca'] + to, msg.as_string())
	except:
		seterr('/email', 'nosend')
	redirect('/', 303)