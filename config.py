from bottle import Bottle, view, request, redirect
import os

app = Bottle()
# config goes in instanceconfig.py
config = """
# this is a python module with configuration details for this instance of hvsi
"""

# 1: configure static file hostname, debug
# 2: configure database
# 3: configure accounts
# 4: configure lang

@app.get('/')
@view('setup_index')
def view_index():
	pass

@app.get('/1')
@view('setup_1')
def view_setup_1():
	pass

@app.post('/1')
def do_setup_1():
	host = request.params.get('host', 'hvsi.ca')
	statichost = request.params.get('statichost', '[app]')
	if statichost == '':
		statichost = '[app]'
	debug = request.params.get('debug', False)
	config += """
host	   = %r
statichost = %r
debug      = %r""" % (host, statichost, debug)
	redirect('2')

@app.get('/2')
@view('setup_2')
def view_setup_2():
	pass

@app.post('/2')
def do_setup_2():
	proto = request.params.get('dbproto', 'mysql')
	host = request.params.get('dbhost', 'localhost')
	user = request.params.get('dbuser', 'hvsi')
	passw =request.params.get('dbpass', 'hvsi')
	db   = request.params.get('dbdb', 'hvsi')
	config += """
dbprot = %r
dbhost = %r
dbuser = %r
dbpass = %r
dbdb   = %r""" % (proto, host, user, passw, db)
	redirect('2.5')

@app.get('/2.5')
@view('setup_confirm_basic')
def view_setup_25():
	return dict(config=config)

@app.post('/2.5')
def do_setup_25():
	f = open(os.path.join(os.getcwd(), 'instanceconfig.py'), 'w')
	f.write(config)
	f.close()
	redirect('3')

@app.get('/3')
@view('setup_3')
def view_setup_3():
	import database

@app.post('/3')
def do_setup_3():
	name = request.params.get('name', 'Admin')
	username = request.params.get('username', 'admin')
	email = request.params.get('email', 'admin@hvsi.ca')
	passw = request.params.get('password', 'admin')
	confirm = request.params.get('confirm', 'admin')
	# passwords don't match? Set to admin and move on
	if passw != confirm:
		passw = 'admin'
	import database
	database.Admin(name=name, username=username, email=email, hashed_pass=passw)
	redirect('4')

@app.get('4')
@view('setup_4')
def view_setup_4():
	pass

@app.post('4')
def do_setup_4():
	redirect('done')

@app.get('/done')
@view('setup_done')
def view_setup_done():
	pass

from bottle import run
run(app, port=9055)