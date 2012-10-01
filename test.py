from bottle import route, view, run
import bottle
bottle.debug(True)
class Req():
	def __init__(self):
		self.logged_in = False
@route('/')
@view('registration')
def index():
	return dict(lang='e',request=Req(),twitter='Twitter feed',page='page')

run(port=9055)
