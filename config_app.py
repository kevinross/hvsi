from bottle import Bottle, template, request, redirect, SimpleTemplate
import os, sys, bottle
import pkg_resources
# all the pages
SimpleTemplate.global_config('from_pkg', 'hvsi')
SimpleTemplate.defaults['bottle'] = bottle
def view(view_name):
	def tview(func):
		def view_func(*args, **kwargs):
			val = func(*args, **kwargs)
			if val is not None and isinstance(val, dict) and 'page' not in val:
				val['page'] = view_name
			return template(view_name, template_settings=dict(from_pkg='hvsi'), **val)
		return view_func
	return tview
libdir = os.path.join(os.getcwd(), 'lib')
sys.path.append(libdir)
if os.path.exists(libdir):
	sys.path.extend([os.path.join(os.getcwd(), 'lib', x) for x in os.listdir(libdir)])

app = Bottle()
# config goes in instanceconfig.py
config = """
# this is a python module with configuration details for this instance of hvsi
"""
aws_sql = """
import os
dbprot		= 'mysql'
dbhost		= os.environ['RDS_HOSTNAME']
dbport		= 3306
dbdb		= os.environ['RDS_DB_NAME']
dbuser		= os.environ['RDS_USERNAME']
dbpass		= os.environ['RDS_PASSWORD']

"""
af_sql = """
import os, simplejson
data		= simplejson.loads(os.environ['VCAP_SERVICES'])['mysql-5.1'][0]['credentials']
dbprot		= 'mysql'
dbhost		= data['hostname']
dbport		= 3306
dbdb		= data['name']
dbuser		= data['username']
dbpass		= data['password']
"""
# 1: module deps
# 2: configure static file hostname, debug, timezone
# 3: configure exception logging
# 4: configure database
# 5: configure lang

langs = ['en-US']

@app.get('/')
@view('setup_index')
def view_index():
	return dict()

def get_unavailable_mods():
	try:
		modules = [x.key for x in pkg_resources.working_set.by_key['hvsi'].requires()]
	except:
		try:
			modules = open('requirements.txt').readlines()
		except:
			modules = open('hvsi/requirements.txt').readlines()
	failed = []
	for module in modules:
		mod = module.replace('\n','').lower()
		if mod == 'mysql-python':
			mod = 'MySQLdb'
		if mod == 'py-bcrypt':
			mod = 'bcrypt'
		try:
			__import__(mod)
		except:
			failed.append(module.replace('\n',''))
	return failed
@app.get('/1')
@view('setup_mods')
def view_setup_mods():
	return dict(failed=get_unavailable_mods(),path=os.path.join(os.getcwd(), 'lib'))

@app.post('/1.5')
@view('setup_do_attempt_mods')
def do_setup_attempt_mods():
	import pkg_resources
	from setuptools.dist import Distribution
	mods = get_unavailable_mods()
	failed = []
	p = os.getcwd()
	if not os.path.exists(libdir):
		os.mkdir(libdir)
	os.chdir(libdir)
	for mod in mods:
		m = mod
		if m == 'MySQLdb':
			m = 'mysql-python'
		if m == 'bcrypt':
			m = 'py-bcrypt'
		try:
			print 'installing %s' % m
			pkg_resources.working_set.resolve(pkg_resources.parse_requirements(m),installer=Distribution().fetch_build_egg)
			print 'done'
		except:
			failed.append(mod)
	os.chdir(p)
	sys.path.extend([os.path.join(p, 'lib', x) for x in mods])
	return dict(failed=failed)


@app.get('/2')
@view('setup_2')
def view_setup_2():
	return dict()

@app.post('/2')
def do_setup_2():
	global config
	host = request.params.get('host', 'hvsi.ca')
	statichost = request.params.get('statichost', '')
	external = request.params.get('externalhost','')
	timezone = request.params.get('timezone','America/Toronto')
	if statichost == 'external':
		statichost = external
	else:
		statichost = None
	debug = request.params.get('debug', False)
	if debug == 'yes':
		debug = True
	else:
		debug = False
	config += """
host		= %r
statichost	= %r
debug		= %r
timezone	= %r""" % (host, statichost, debug, timezone)
	# production uses error reporting, so redirect to that if in production mode
	# else, skip it as a different system is used
	if not debug:
		redirect('3')
	redirect('4')

@app.get('/3')
@view('setup_3')
def view_setup_3():
	return dict()

@app.post('/3')
def do_setup_3():
	mode = request.params.get('exceptions', 'file')
	global config
	# if exceptionpath is null, errormiddleware won't log to path
	# if to address is null, errormiddleware won't log to email
	if mode == 'file' or mode == 'both':
		path = request.params.get('file',None)
	else:
		path = None
	if mode == 'email' or mode == 'both':
		p = request.params
		t = p['to']
		f = p['from']
		s = p['server']
		u = p['username']
		pa = p['password']
	else:
		t = f = s = u = pa = None
	config += """
exceptionpath 	= %r
smtp_to		= %r
smtp_from	= %r
smtp_server	= %r
smtp_user	= %r
smtp_pass	= %r""" % (path, t, f, s, u, pa)
	redirect('/4')


@app.get('/4')
@view('setup_4')
def view_setup_4():
	return dict(has_mysql=("MySQLdb" not in get_unavailable_mods()))

@app.post('/4')
def do_setup_4():
	global config
	infra = request.params.get('infra', 'custom')
	proto = request.params.get('dbproto', 'mysql')
	host = request.params.get('dbhost', 'localhost')
	try:
		port = int(request.params.get('dbport', 3306))
	except:
		port = 3306 if proto == 'mysql' else 5432
	user = request.params.get('dbuser', 'hvsi')
	passw =request.params.get('dbpass', 'hvsi')
	db   = request.params.get('dbdb', 'hvsi')
	if infra == 'custom':
		config += """
dbprot		= %r
dbhost		= %r
dbport		= %r
dbuser		= %r
dbpass		= %r
dbdb		= %r""" % (proto, host, port, user, passw, db)
	elif infra == 'aws':
		config += aws_sql
	elif infra == 'af':
		config += af_sql
	redirect('4.5')

@app.get('/4.5')
@view('setup_confirm_basic')
def view_setup_45():
	return dict(config=config)

@app.post('/4.5')
def do_setup_45():
	f = open(os.path.join(os.getcwd(), 'instanceconfig.py'), 'w')
	config = request.params['config']
	f.write(config)
	f.close()
	redirect('5')


@app.get('/5')
@view('setup_5')
def view_setup_5():
	global langs
	return dict(langs=langs)

@app.post('/5.u')
def update_setup_5():
	global langs
	langs.append(request.params['lang_short'])
	redirect('5')

@app.post('/5')
def do_setup_5():
	global langs
	import shutil
	for lang in [x for x in langs if x != 'en-US']:
		if not os.path.exists('i18n_%s.py' % lang):
			shutil.copyfile('i18n_en_US.py', 'i18n_%s.py' % lang.replace('-','_'))
	redirect('done')


@app.get('/done')
@view('setup_done')
def view_setup_done():
	return dict()

#from bottle import run
#run(app, port=9055)