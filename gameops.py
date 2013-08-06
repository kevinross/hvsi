from decorators import *
from database import *
from controller import error, seterr
from ops import *
import i18n, ops, random, string
from bottle import route, request, redirect
@route('/tag',method='GET')
@mview('tag')
@allow_auth
@lang
@require_auth
def view_tag():
	return dict(# copy station errors to tag
		i18n=i18n.i18n_over({'e':{'pages':{'tag':i18n.i18n['e']['pages']['station']['errors']}},
							 'f':{'pages':{'tag':i18n.i18n['f']['pages']['station']['errors']}}}
		))
@route('/tag',method='POST')
@allow_auth
@require_auth
def do_tag():
	if 'taggee' not in request.params:
		seterr('/tag','badinput')
	if 'uid' not in request.params:
		seterr('/tag','badinput')
	if not Game.is_started:
		seterr('/tag','game')
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
		seterr('/tag', error)
	else:
		redirect(request.environ.get('HTTP_REFERER','/'), 303)

@route('/webcheckin')
@mview('webcheckin')
@allow_auth
@lang
@require_auth
@require_role(Player)
def view_webcheckin():
	return dict()
@route('/webcheckin',method='POST')
@allow_auth
@require_auth
@require_role(Player)
def do_webcheckin():
	p = request.params
	if 'confirm' not in p:
		redirect('/webcheckin?error=notconfirmed', 303)
	if request.user.did_webcheckin:
		redirect('/webcheckin?error=alreadyused', 303)
	station = Account.get_user('zombie_internet')
	if not station:
		redirect('/webcheckin?error=code499', 303)
	try:
		do_checkin(request.user, station)
	except CheckInException, e:
		err = e.message[::-1]
		err = err[:err.find(' ')][::-1]
		seterr('/webcheckin', err)
	redirect('/', 303)

@route('/station')
@mview('station')
@allow_auth
@lang
@require_auth
@require_role(Admin, Station)
def view_stationops():
	if 'section' in request.params:
		request.session.error = 'generic'
		return dict(section=request.params['section'],err=request.params['err'],error='err' in request.params, page='station',post=Post.from_pid(5))
	return dict(post=Post.from_pid(5))
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
	redirect('/station', code=303)

@route('/station/activate', method='POST')
@allow_auth
@require_auth
@require_role(Admin,Station)
def do_station_activate():
	if 'user_id' not in request.params:
		redirect('/station?section=activate&err=nouid', 303)
	try:
		i = int(request.params['user_id'])
	except:
		redirect('/station?section=activate&err=nouid', 303)
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