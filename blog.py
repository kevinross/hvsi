from decorators import *
from database import *
from controller import error, seterr
from bottle import request, redirect, route
import datetime, bottle, simplejson, i18n
@route('/post/view/:pid')
@mview('index')
@allow_auth
@lang
def view_post(pid):
	try:
		p = Post.from_pid(pid)
		return dict(post=p,i18n=i18n.override_title('index',p.title_e,p.title_f))
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
		seterr('/post/view/%s' % str(pid), 'nocontent')
	if Comment.select(Comment.q.user == request.user and Comment.q.content == p['comment']).count() > 0:
		seterr('/post/view/%s' % str(pid), 'exists')
	c = Comment(user=request.user, content=p['comment'], post=po)
	redirect('/post/view/' + str(pid) + '#comment-' + str(c.id), 303)
@route('/post/create',method='GET')
@mview('create_editpost')
@allow_auth
@lang
@require_auth
@require_role(Admin)
def view_create_post():
	return dict(mode='create')

@route('/post/create',method='POST')
@allow_auth
@require_auth
@require_role(Admin)
def do_create_post():
	p = request.params
	# content_e, content_f, title_e, title_f
	if not p['content_e'] or not p['content_f'] or not p['title_e'] or not p['title_f']:
		bottle.request.session.data = simplejson.dumps(p)
		seterr('/post/create','missinginfo')
	if 'allow_comments' in p:
		p['allow_comments'] = True
	else:
		p['allow_comments'] = False
	p = dict([(x,p[x]) for x in ['content_e','content_f','title_e','title_f','allow_comments']])
	post = Post(allow_comments=p['allow_comments'])
	for k in p:
		setattr(post, k, p[k])
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
		return dict(post=p,mode='edit',
					i18n=i18n.override_title('create_editpost','Editing EN:"' + p.title_e + '" FR:"' + p.title_f + '"','Editing "' + p.title_f + '"'))
	except IndexError, e:
		request.session.error = 'nopostpid'
		return dict(error='nopostpid',mode='edit')
	except:
		request.session.error = 'unknown'
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
		error(code=404)
	except:
		seterr(request.path, 'unknown')
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
def do_delete_post(pid):
	try:
		p = Post.from_pid(pid)
	except IndexError, e:
		return
	p.delete()
	redirect('/', 303)