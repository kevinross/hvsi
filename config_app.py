from bottle import Bottle, view, request, redirect
import os, sys
libdir = os.path.join(os.getcwd(), 'lib')
sys.path.append(libdir)
sys.path.extend([os.path.join(os.getcwd(), 'lib', x) for x in os.listdir(libdir)])

app = Bottle()
# config goes in instanceconfig.py
config = """
# this is a python module with configuration details for this instance of hvsi
"""
# 1: module deps
# 2: configure static file hostname, debug, timezone
# 3: configure database
# 4: configure lang

langs = ['en-US']

@app.get('/')
@view('setup_index')
def view_index():
	return dict()

def get_unavailable_mods():
	f = open('requirements.txt')
	modules = f.readlines()
	f.close()
	failed = []
	for module in modules:
		mod = module.replace('\n','').lower()
		if mod == 'mysql-python':
			mod = 'MySQLdb'
			os.environ['DYLD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] = '/usr/local/mysql/lib'
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
	exceptionpath = request.params.get('exceptionlogs', None)
	if exceptionpath == '':
		exceptionpath = None
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
host			= %r
statichost		= %r
debug			= %r
exceptionpath	= %r
timezone		= %r""" % (host, statichost, debug, exceptionpath, timezone)
	redirect('3')

@app.get('/3')
@view('setup_3')
def view_setup_3():
	return dict(has_mysql=("MySQLdb" not in get_unavailable_mods()))

@app.post('/3')
def do_setup_3():
	global config
	proto = request.params.get('dbproto', 'mysql')
	host = request.params.get('dbhost', 'localhost')
	user = request.params.get('dbuser', 'hvsi')
	passw =request.params.get('dbpass', 'hvsi')
	db   = request.params.get('dbdb', 'hvsi')
	config += """
dbprot			= %r
dbhost			= %r
dbuser			= %r
dbpass			= %r
dbdb			= %r""" % (proto, host, user, passw, db)
	redirect('3.5')

@app.get('/3.5')
@view('setup_confirm_basic')
def view_setup_35():
	return dict(config=config)

@app.post('/3.5')
def do_setup_35():
	f = open(os.path.join(os.getcwd(), 'instanceconfig.py'), 'w')
	config = """import os, sys, simplejson
libdir = os.path.join(os.getcwd(), 'lib')
sys.path.append(libdir)
sys.path.extend([os.path.join(os.getcwd(), 'lib', x) for x in os.listdir(libdir)])

""" + request.params['config'] + """
if 'VCAP_SERVICES' in os.environ:
	d = simplejson.loads(os.environ['VCAP_SERVICES'])['mysql-5.1'][0]['credentials']
	dbprot = 'mysql'
	dbhost = d['hostname']
	dbdb = d['name']
	dbuser = d['username']
	dbpass = d['password']
"""
	f.write(config)
	f.close()
	redirect('4')


@app.get('/4')
@view('setup_4')
def view_setup_4():
	global langs
	return dict(langs=langs)

@app.post('/4.u')
def update_setup_4():
	global langs
	langs.append(request.params['lang_short'])
	redirect('4')

@app.post('/4')
def do_setup_4():
	global langs
	import shutil
	for lang in langs:
		if not os.path.exists('i18n_%s.py' % lang):
			shutil.copyfile('i18n_en_US.py', 'i18n_%s.py' % lang.replace('-','_'))
	redirect('done')


@app.get('/done')
@view('setup_done')
def view_setup_done():
	os.rename('config_app.py','disabled_configurator_app')
	return dict()

from bottle import run
run(app, port=9055)