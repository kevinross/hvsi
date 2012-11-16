from decorators import *
from database import *
from controller import error, seterr
import i18n, datetime, database
from bottle import route, request, redirect
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
	user = Account.get_user(name)
	if not user:
		error(code=404)
	return dict(vuser=user,i18n=i18n.override_title('user',user.username,user.username))

@route('/user/:name/edit',method='GET')
@mview('user_edit')
@allow_auth
@lang
@require_auth
@require_role(Admin,Player)
def view_user_edit(name):
	if not request.admin and request.user.username != name:
		error(code=401)
	user = Account.get_user(name)
	if not user:
		error(code=404)
	return dict(vuser=user,
				i18n=i18n.override_title('user_edit',
										 i18n.i18n['e']['pages']['user_edit']['editing'] + ' ' + user.username,
										 i18n.i18n['f']['pages']['user_edit']['editing'] + ' ' + user.username))

@route('/user/:name/edit',method='POST')
@allow_auth
@require_auth
@require_role(Admin,Player)
def do_user_edit(name):
	if not request.admin and request.user.username != name:
		error(code=401)
	p = request.params
	user = Account.get_user(name)
	# whitelist the paras a player may pass in
	perm_user = ['verify_password','password','confirm_password','language','cell','twitter','email']
	if request.player:
		# filter the params down to the permitted ones
		p = dict([(x,p[x]) for x in perm_user if x in p])
	if 'password' in p and p['password'] and not request.admin:
		if p['password'] != p['confirm_password']:
			seterr('/user/%s/edit' % name, 'vp')
		if not user.verify_pass(p['verify_password']):
			seterr('/user/%s/edit' % name, 'bp')
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
	user = Account.get_user(name)
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
	u = Account.get_user(name)
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
	user = Account.get_user(name)
	if not user:
		error(code=404)
	if 'username' not in request.params:
		seterr('/station', 'noplayer')
	redirect('/'.join(['/tag',name,request.params['username']]), 303)

@route('/user/:name/checkins',method='GET')
@mview('checkins')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_user_checkins(name):
	user = Account.get_user(name)
	if not user:
		error(code=404)
	return dict(vuser=user,checkins=user.checkins.orderBy(Checkin.q.time))
@route('/user/:name/checkins/add',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_add_user_checkin(name):
	user = Account.get_user(name)
	if not user:
		error(code=404)
	# no location or time
	if not 'location' in request.params:
		seterr('/user/%s/checkins' % user.username, 'noloc')
	if not 'time' in request.params:
		seterr('/user/%s/checkins' % user.username, 'notime')
	# bad location
	if not request.params['location'] in database.locations:
		seterr('/user/%s/checkins' % user.username, 'badloc')
	# bad time
	time = None
	try:
		time = datetime.datetime.strptime(request.params['time'],'%Y-%m-%d %H:%M:%S')
	except:
		seterr('/user/%s/checkins' % user.username, 'badtime')
	location = request.params['location']
	Checkin(time=time,location=location,player=user)
	redirect('/user/%s/checkins' % name, 303)
@route('/user/:name/checkins/delete',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_del_user_checkins(name):
	user = Account.get_user(name)
	if not user:
		error(code=404)
	# checkins are like checkin_[id]
	ids = [int(x[x.find('_')+1:]) for x in request.params if 'checkin_' in x]
	_ = [Checkin.select(Checkin.q.id == x)[0].destroySelf() for x in ids]
	redirect('/user/%s/checkins' % user.username, 303)