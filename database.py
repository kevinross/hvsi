from sqlobject import *
from sqlobject.mysql import builder
from sqlobject.inheritance import *
from sqlobject_todict import to_dict
import bcrypt, datetime, time, markdown, os, urllib, uuid, hashlib, simplejson
__all__ = ['Game','Account','Player','Bounty','Station','Admin','Tag','Checkin','Cure','Post','Comment', 'DbString','Snapshot','Score','Session','PasswordReset']
NAMESPACE = 'hvsi'
from settings import instanceconfig
proto = instanceconfig.dbprot
host = instanceconfig.dbhost
port = instanceconfig.dbport
db = instanceconfig.dbdb
user = instanceconfig.dbuser
passw = instanceconfig.dbpass
if proto == 'sqlite':
	sqlhub.processConnection = connectionForURI('sqlite:%s/%s' % (host, db))
else:
	sqlhub.processConnection = connectionForURI('%s://%s:%s@%s:%i/%s' % (proto, user, passw, host, port, db))
if instanceconfig.debug:
	sqlhub.processConnection.debug = True
	sqlhub.processConnection.debugOutput = True
def norm_cell(val):
	# strip everything out leaving just the numbers.
	# prefix with a 1 if not already done
	if not val:
		return ''
	final = ''
	for i in val:
		if i == '@':
			break
		if i in '0123456789':
			final += i
	if not final:
		return None
	if final[0] != '1':
		final = '1' + final
	return final
class Dictable():
	@property
	def dict(self):
		return to_dict(self)

class Game(SQLObject,Dictable):
	class sqlmeta:
		registry = NAMESPACE
	max_id		= 12+1
	started		= BoolCol(default=False)
	time		= DateTimeCol(default=datetime.datetime.now)
	string		= StringCol(default=None)
	number		= IntCol(default=None)
	def _set_started(self, val):
		self.time = datetime.datetime.now()
		self._SO_set_started(val)
	class started_class(object):
		def __init__(self, index):
			self.i = index
		def __get__(self, obj, objtype):
			try:
				return Game.select(Game.q.id == self.i)[0].started
			except:
				return Game(id=self.i).started
		def __set__(self, obj, value):
			try:
				Game.select(Game.q.id == self.i)[0].started = value
				Game.select(Game.q.id == self.i)[0].time = datetime.datetime.now()
			except:
				g = Game(id=self.i)
				g.started = value
				g.time = datetime.datetime.now()
	class value_class(object):
		def __init__(self, attr, index):
			self.i = index
			self.attr = attr
		def __get__(self, obj, objtype):
			try:
				return getattr(Game.select(Game.q.id == self.i)[0], self.attr)
			except:
				g = Game(id=self.i)
				return getattr(g, self.attr)
		def __set__(self, obj, value):
			try:
				setattr(Game.select(Game.q.id == self.i)[0], self.attr, value)
			except:
				g = Game(id=self.i)
				setattr(g, self.attr, value)
	is_started = started_class(1)
	is_reg	   = started_class(2)
	game_start = value_class('time',3)
	game_end   = value_class('time',4)
	game_rego  = value_class('time',5)
	it_email   = value_class('string',6)
	hours_between_checkins = value_class('number',7)
	is_countdown  = started_class(8)
	countdown_time = value_class('time',9)
	email_host = value_class('string',10)
	email_user = value_class('string',11)
	email_pass = value_class('string',12)
	@staticmethod
	def toggle_game():
		Game.select(Game.q.id == 1)[0].started = not Game.select(Game.q.id == 1)[0].started
	@staticmethod
	def toggle_reg():
		Game.select(Game.q.id == 2)[0].started = not Game.select(Game.q.id == 2)[0].started
	@staticmethod
	def toggle_countdown():
		Game.select(Game.q.id == 8)[0].started = not Game.select(Game.q.id == 8)[0].started
GameClass = Game
try:
	Game = Game.select()[0]
except:
	pass

DEFAULT_LIFETIME = 300
class Session(InheritableSQLObject,Dictable):
	class sqlmeta:
		registry = NAMESPACE
	skey		 = StringCol(length=32,varchar=True,unique=True,notNone=True,default=lambda:uuid.uuid4().get_hex())
	expires		 = DateTimeCol(notNone=True,default=lambda:datetime.datetime.now()+datetime.timedelta(0,DEFAULT_LIFETIME))
	ttl			 = IntCol(default=DEFAULT_LIFETIME)
	language	 = StringCol(default='e')
	user		 = ForeignKey('Account',default=None)
	error		 = StringCol(default=None)
	data		 = StringCol(default=None)

	@classmethod
	def grab(cls, key, attr='skey'):
		s = cls.select(getattr(cls.q, attr) == key)[0]
		if not isinstance(s, cls):	# guards against people using password reset hashes as sessions as
			s.destroySelf()			# sqlobject automatically converts to subclasses so a select() on Session
			s = cls()				# could return a password reset
		u = s.user
		if s.expired:		# expired
			# destroy and expire it
			s.destroySelf()
			s = Session(user=u)
		s.update_expires()
		return s

	@property
	def expired(self):
		return datetime.datetime.now() > self.expires

	def update_expires(self):
		self.expires = datetime.datetime.now() + datetime.timedelta(0, self.ttl)

	@staticmethod
	def session(user):
		u = user
		if isinstance(u, basestring):
			u = Account.get_user(u)
		if not u:
			return None
		if Session.select(Session.q.user == u).count() == 0:
			s = Session(user=u)
		else:
			s = Session.grab(u, 'user')
		return s

	@property
	def data_dict(self):
		if not self.data:
			self.data = '{}'
		return simplejson.loads(self.data)

	def __getitem__(self, item):
		return simplejson.loads(self.data)[item]

	def __setitem__(self, key, value):
		d = self.data_dict
		d[key] = value
		self.data = simplejson.dumps(d)

class PasswordReset(Session):
	class sqlmeta:
		registry = NAMESPACE


class Account(InheritableSQLObject,Dictable):
	class sqlmeta:
		registry = NAMESPACE
		createSQL = {'mysql': [
			'ALTER TABLE account MODIFY username VARCHAR(25) COLLATE latin1_general_cs',
			'ALTER TABLE account MODIFY name VARCHAR(25) COLLATE latin1_general_cs'
		]}
	name		 = StringCol(length=25,varchar=True,notNone=True)
	username	 = StringCol(length=25,varchar=True,unique=True,notNone=True)
	hashed_pass	 = StringCol(notNone=True)
	language	 = StringCol(default='e')
	email		 = StringCol(length=50,varchar=True,unique=True,notNone=True)
	creation_time= DateTimeCol(default=datetime.datetime.now)
	def to_dict(self):
		return dict([(x,getattr(self, x)) for x in self.sqlmeta.columns if
						(not isinstance(self.sqlmeta.columns[x], SOForeignKey) and not self.sqlmeta.columns[x].name == 'childName')])
	def _set_hashed_pass(self, pas):
		self._SO_set_hashed_pass(bcrypt.hashpw(pas, bcrypt.gensalt()))
	def verify_pass(self, pas):
		return self.hashed_pass == bcrypt.hashpw(pas, self.hashed_pass)
	def change_pass(self, old, new):
		if not self.verify_pass(old):
			return False
		self.hashed_pass = new
		return True
	@staticmethod
	def from_id(num):
		try:
			return Account.select(Account.q.id == num)[0]
		except:
			return None
	@staticmethod
	def from_username(uname):
		try:
			return Account.select(Account.q.username == uname)[0]
		except:
			return None
	@staticmethod
	def from_email(email):
		try:
			return Account.select(Account.q.email == email)[0]
		except:
			return None
	@staticmethod
	def get_user(v):
		if isinstance(v, Account):
			return v
		elif isinstance(v, str):
			return Account.from_username(v) or Account.from_email(v)
		elif isinstance(v, int):
			return Account.from_id(v)
locations = ['cby','ucu','cafealt','manual','twitter','email','internet','admin','unset']
states = ['human','zombie','inactive','banned']
class Player(Account):
	class sqlmeta:
		registry = NAMESPACE
		createSQL = {'mysql': [
			'ALTER TABLE player ALTER signedin SET DEFAULT 0',
			'ALTER TABLE player ALTER liability SET DEFAULT 0',
			'ALTER TABLE player ALTER safety SET DEFAULT 0',
			'ALTER TABLE player ALTER zero SET DEFAULT 0'
		]}
	student_num	 	 = IntCol(unique=True,notNone=True)
	twitter		 	 = StringCol(length=50,varchar=True,unique=True,default=None)
	cell		 	 = StringCol(length=11,varchar=True,unique=True,default=None)
	state			 = EnumCol(enumValues=states,default='human',notNone=True)
	game_id			 = StringCol(length=10,varchar=True,unique=True,default=None)
	kills			 = SQLMultipleJoin('Tag',joinColumn='tagger_id')
	deaths			 = SQLMultipleJoin('Tag',joinColumn='taggee_id')
	checkins		 = SQLMultipleJoin('Checkin',joinColumn='player_id',orderBy='time')
	cures			 = SQLMultipleJoin('Cure',joinColumn='player_id',orderBy='time')
	signedin		 = BoolCol(default=False, notNone=True)
	signedin_time	 = DateTimeCol(default=None)
	liability		 = BoolCol(default=False, notNone=True)
	safety			 = BoolCol(default=False, notNone=True)
	zero			 = BoolCol(default=False, notNone=True)
	def _set_zero(self, zero):
		# subtle bug here.  If creating the first Player in the db, the class won't have an ID column yet
		# so if there aren't any players yet, just set zero and return
		if sqlhub.processConnection.queryOne('SELECT COUNT(*) FROM player')[0] == 0:
			self._SO_set_zero(False)
			return
		# if I don't exist yet...
		if self.sqlmeta._creating:
			self._SO_set_zero(False)
			return
		for i in Player.select(Player.q.id != self.id):
			i._SO_set_state('human')
			i._SO_set_zero(False)
		self._SO_set_zero(True)
	def _set_state(self, state):
		self._SO_set_state(state)
		try:
			if self.signedin:
				Snapshot(changer=self)
		except:
			pass
	def _get_game_id(self):
		# surprise! the game_id isn't completely random at all!
		if not self._SO_get_game_id():
			i = ('H' + hashlib.sha512(''.join([self.name,self.username,str(self.student_num),str(time.clock())])).hexdigest()[16:24] + 'Z').upper()
			self._SO_set_game_id(i)
		return self._SO_get_game_id()
	def _set_game_id(self, val):
		# attribute is immutable
		return
	def _set_cell(self, val):
		self._SO_set_cell(None if not val else norm_cell(val))
	def _set_signedin(self, v):
		self._SO_set_signedin(v)
		if v:
			Snapshot(changer=self)		# add a snapshot, new user!!
			self.signedin_time = datetime.datetime.now()
	def _get_last_checkin(self):
		try:
			return self.checkins[-1]
		except:
			return None
	def _get_last_checkin_time(self):
		try:
			return self.checkins[-1].time
		except:
			return None
	def _get_last_checkin_loc(self):
		try:
			return self.checkins[-1].location
		except:
			return None
	def _get_did_webcheckin(self):
		try:
			return self.checkins.filter(Checkin.q.location==Checkin.location_internet).count() > 0
		except:
			return False
	def _get_last_death(self):
		try:
			return self.deaths[-1]
		except:
			return None
	def _get_last_kill(self):
		try:
			return self.kills[-1]
		except:
			return None
	def _get_last_cure(self):
		try:
			return self.cures[-1]
		except:
			return None
	def is_cured(self):
		return self.cures.count() > 0
	def is_zombie(self):
		return self.state == self.state_zombie
	def is_human(self):
		return self.state == self.state_human
	def kill(self):
		self.state = self.state_zombie
	def cure(self):
		self.state = self.state_human
	@staticmethod
	def from_twitter(twit):
		if not twit:
			return None
		try:
			return Account.select(Account.q.twitter == twit)[0]
		except:
			return None
	@staticmethod
	def from_student_num(num):
		try:
			return Account.select(Account.q.student_num == num)[0]
		except:
			return None
	@staticmethod
	def from_cell(cell):
		if not cell:
			return None
		cell = norm_cell(cell)
		if not cell:
			return None
		try:
			return Account.select(Account.q.cell == cell)[0]
		except:
			return None
	@staticmethod
	def from_game_id(gid):
		try:
			return Player.select(Player.q.game_id == gid)[0]
		except:
			return None
	@staticmethod
	def get_player(v):
		# cell phones using email
		if isinstance(v, str) and '@' in v:
			try:
				i = int(v[:v.find('@')])
				if len(str(i)) >= 10:
					v = str(i)
			except:
				pass
		# prefer student num over cell phone
		try:
			i = int(v)
			p = Player.from_student_num(i) or Player.from_cell(str(i))
			if p:
				return p
		except:
			pass
		return v if isinstance(v,Player) else (Player.from_username(v) or Player.from_game_id(v) or Player.from_twitter(v) or Player.from_email(v))
	class state_class(object):
		def __init__(self, state):
			self.state = state
		def __get__(self, obj, objtype):
			# military part excludes the military bot from normal operations
			return Player.select(Player.q.state == self.state).filter(Player.q.signedin == True).filter(Player.q.username != "military.militaire")
	class state_class2(object):
		def __get__(self, obj, objtype):
			# military part excludes the military bot from normal operations
			return Player.select().filter(Player.q.username != "military.militaire")
	humans  = state_class('human')
	zombies = state_class('zombie')
	users = state_class2()

class Bounty(Player):
	class sqlmeta:
		registry = NAMESPACE
	def _set_state(self, val):
		self._SO_set_state(val)
class Station(Account):
	class sqlmeta:
		registry = NAMESPACE
	location		 = EnumCol(enumValues=locations,default='unset',notNone=True)
class Admin(Account):
	class sqlmeta:
		registry = NAMESPACE
	def _get_location(self):
		return Station.location_admin
class Tag(SQLObject,Dictable):
	class sqlmeta:
		registry = NAMESPACE
	time	= DateTimeCol(default=datetime.datetime.now,notNone=True)
	tagger	= ForeignKey('Player',notNone=True)
	taggee  = ForeignKey('Player',notNone=True)
	# prevents spoofing of tags
	uid		= StringCol(length=100,varchar=True,unique=True,notNone=True)
	def _get_method(self):
		try:
			i = int(self.uid)
			return 'twitter'
		except:
			pass
		if '_' in self.uid:
			return self.uid[:self.uid.find('_')]
		if '@' in self.uid:
			return 'email'
		return 'unknown'
	@staticmethod
	def from_uid(uid):
		return Tag.select(Tag.q.uid == uid)[0]
	@staticmethod
	def has_uid(uid):
		return Tag.select(Tag.q.uid == uid).count() > 0
	@staticmethod
	def for_user(u):
		return Tag.select(OR(Tag.q.tagger == u, Tag.q.taggee == u))
class Checkin(SQLObject,Dictable):
	class sqlmeta:
		registry = NAMESPACE
	time	= DateTimeCol(default=datetime.datetime.now,notNone=True)
	location= EnumCol(enumValues=locations,notNone=True)
	player	= ForeignKey('Player',notNone=True)
class Cure(SQLObject,Dictable):
	class sqlmeta:
		registry = NAMESPACE
	time		= DateTimeCol(default=datetime.datetime.now,notNone=True)
	expiry		= DateTimeCol()
	card_id 	= StringCol(length=10,varchar=True,unique=True,default=None)
	used		= BoolCol(default=False,notNone=True)
	disqualified= BoolCol(default=False,notNone=True)
	player		= ForeignKey('Player',default=None)
	def _get_card_id(self):
		# surprise! the game_id isn't completely random at all!
		if not self._SO_get_card_id():
			self._SO_set_card_id(hashlib.sha512(''.join([self.time.isoformat(),str(self.used),str(self.disqualified),str(time.clock())])).hexdigest()[15:25])
		return self._SO_get_card_id()
	@staticmethod
	def from_cure_id(v):
		try:
			return Cure.select(Cure.q.card_id == v)[0]
		except:
			return None
	@staticmethod
	def from_id(uid):
		try:
			return Cure.select(Cure.q.id == uid)[0]
		except:
			return None
	@staticmethod
	def get_cure(v):
		if isinstance(v, Cure):
			return v
		elif isinstance(v, str):
			return Cure.from_cure_id(v)
		elif isinstance(v, int):
			return Cure.from_id(v)
	class state_class(object):
		def __init__(self, used):
			self.used = used
		def __get__(self, obj, objtype):
			return Cure.select(Cure.q.used == self.used)
	used_cards = state_class(True)
	unused_cards = state_class(False)
class DbString(SQLObject, Dictable):
	class sqlmeta:
		registry = NAMESPACE
	lang			= StringCol()
	field			= StringCol()
	content			= UnicodeCol()
	post			= ForeignKey('Post')

class string_dict():
	def __init__(self, inst, attr):
		self.inst = inst
		self.attr = attr
	def __getitem__(self, item):
		return getattr(self.inst, '_SO_get_' + self.attr)().filter(DbString.q.field == self.attr).filter(DbString.q.lang == item)[0].content
	def __setitem__(self, item, val):
		getattr(self.inst, '_SO_get_' + self.attr)().filter(DbString.q.field == self.attr).filter(DbString.q.lang == item)[0].content = val
class Post(SQLObject,Dictable):
	class sqlmeta:
		registry = NAMESPACE
	time			= DateTimeCol(default=datetime.datetime.now,notNone=True)
	title			= SQLMultipleJoin('DbString',joinColumn='post_id')
	content			= SQLMultipleJoin('DbString',joinColumn='post_id')
	allow_comments 	= BoolCol(default=True,notNone=True)
	comments		= SQLMultipleJoin('Comment',joinColumn='post_id',orderBy='time')
	def _get_content(self):
		return self._SO_get_content().filter(DbString.q.field == 'content')
	def _get_title(self):
		return self._SO_get_title().filter(DbString.q.field == 'title')
	def _get_stitle(self):
		return string_dict(self, 'title')
	def _get_scontent(self):
		return string_dict(self, 'content')
	def _get_content_e(self):
		try:
			return self.scontent['e']
		except:
			return ''
	def _get_title_e(self):
		try:
			return self.stitle['e']
		except:
			return ''
	def _get_content_f(self):
		try:
			return self.scontent['f']
		except:
			return ''
	def _get_title_f(self):
		try:
			return self.stitle['f']
		except:
			return ''
	def _set_content_e(self, val):
		try:
			self.scontent['e'] = val
		except:
			c = DbString(lang='e',content=val,field='content',post=self)
	def _set_title_e(self, val):
		try:
			self.stitle['e'] = val
		except:
			c = DbString(lang='e',content=val,field='title',post=self)
	def _set_content_f(self, val):
		try:
			self.scontent['f'] = val
		except:
			c = DbString(lang='f',content=val,field='content',post=self)
	def _set_title_f(self, val):
		try:
			self.stitle['f'] = val
		except:
			c = DbString(lang='f',content=val,field='title',post=self)
	def _get_html_e(self):
		return markdown.markdown(self.content_e,output_format='html')
	def _get_html_f(self):
		return markdown.markdown(self.content_f,output_format='html')
	@staticmethod
	def from_pid(pid):
		return Post.select(Post.q.id == pid)[0]
	def to_dict(self):
		return dict(
			__meta__ = dict(
				name = "PostDict",
				id = self.id
			),
			time = self.time.isoformat(),
			e = dict(
				title = self.title_e,
				content = self.html_e
				),
			f = dict(
				title = self.title_f,
				content = self.content_f
				)
			)
	def delete(self):
		for i in self.comments:
			i.destroySelf()
		for i in self.title:
			i.destroySelf()
		for i in self.content:
			i.destroySelf()
		self.destroySelf()
class Comment(SQLObject,Dictable):
	class sqlmeta:
		registry = NAMESPACE
	time		= DateTimeCol(default=datetime.datetime.now,notNone=True)
	content		= StringCol()
	user		= ForeignKey('Account',notNone=True)
	post		= ForeignKey('Post',notNone=True)
	def _get_html(self):
		return markdown.markdown(self.content, safe_mode="remove")
class Snapshot(SQLObject):
	class sqlmeta:
		registry = NAMESPACE
	time		 = DateTimeCol(default=datetime.datetime.now)
	num_humans	 = IntCol(default=Player.humans.count)
	num_zombies	 = IntCol(default=Player.zombies.count)
	changer		 = ForeignKey('Player',notNone=False)
	class today_class(object):
		def __get__(self, obj, objtype):
			now = datetime.datetime.now()
			morning = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, 0)
			night = datetime.datetime(now.year, now.month, now.day, 23, 59, 59, 999999)
			return Snapshot.select(Snapshot.q.time > morning and Snapshot.q.time < night)
	today = today_class()
	@staticmethod
	def points_after_hour(x):
		now = datetime.datetime.now()
		hour = datetime.datetime(now.year, now.month, now.day, x, 0, 0, 0)
		hour_plus_one = hour + datetime.timedelta(0,0,0,0,0,1)
		return Snapshot.points_between(hour, hour_plus_one)
	@staticmethod
	def points_before_hour(x):
		now = datetime.datetime.now()
		hour = datetime.datetime(now.year, now.month, now.day, x, 0, 0, 0)
		hour_minus_one = hour - datetime.timedelta(0,0,0,0,0,1)
		return Snapshot.points_between(hour_minus_one, hour)
	@staticmethod
	def points_after_date(x):
		return Snapshot.points_between(x, x + datetime.timedelta(0,0,0,0,0,1))
	@staticmethod
	def points_before_date(x):
		return Snapshot.points_between(x - datetime.timedelta(0,0,0,0,0,1), x)
	@staticmethod
	def points_between(a,b):
		return Snapshot.select(Snapshot.q.time > a and Snapshot.q.time < b,orderBy=DESC(Snapshot.q.time))
	class latest_class(object):
		def __get__(self, obj, objtype):
			return Snapshot.select(orderBy=DESC(Snapshot.q.time))[0]
	latest = latest_class()

# used to more efficiently store the scores for each person
# if this didn't exist, we'd have to run a SELECT on Tag and count() for each player,
# that could get slow really quickly
class Score(SQLObject,Dictable):
	class sqlmeta:
		registry = NAMESPACE
	player = ForeignKey('Player')
	kills = IntCol()
	@staticmethod
	def get_scorecard(player):
		try:
			return Score.select(Score.q.player == player)[0]
		except:
			return Score(player=player, kills=player.kills.count())
	class latest_class(object):
		def __get__(self, obj, objtype):
			return Score.select(Score.q.player != Player.get_player('military.militaire'),orderBy=DESC(Score.q.kills))
	top = latest_class()

def set_class_enum(klass, var, array):
	for i in array:
		setattr(klass, var + '_' + i, i)
set_class_enum(Player,'state', states)
set_class_enum(Admin,'location',locations)
set_class_enum(Station,'location',locations)
set_class_enum(Checkin,'location',locations)
def createTables():
	Game.createTable(ifNotExists=True)
	Account.createTable(ifNotExists=True)
	Admin.createTable(ifNotExists=True)
	Station.createTable(ifNotExists=True)
	Player.createTable(ifNotExists=True)
	Tag.createTable(ifNotExists=True)
	Checkin.createTable(ifNotExists=True)
	Cure.createTable(ifNotExists=True)
	Post.createTable(ifNotExists=True)
	Comment.createTable(ifNotExists=True)
	Snapshot.createTable(ifNotExists=True)
	Score.createTable(ifNotExists=True)
	Session.createTable(ifNotExists=True)
	DbString.createTable(ifNotExists=True)
	PasswordReset.createTable(ifNotExists=True)
def create_default_data():
	for i in range(1, 6):
		try:
			Post.get(i)
		except:
			Post(id=i, allow_comments=False)
	if not Account.get_user('admin'):
		a = Admin(name='Admin',username='admin',hashed_pass='admin',email='admin@hvsi.ca')
	if not Account.get_user('military.militaire'):
		p = Player(name='Military / Militaire',username='military.militaire',hashed_pass='asiod8ofa9s8df',
			   student_num=1,email='military@hvsi.ca',state='zombie')
	for i in range(1, Game.max_id):
		try:
			GameClass(id=i)
		except dberrors.DuplicateEntryError, e:
			pass
try:
	if sqlhub.processConnection:
		createTables()
		create_default_data()
except:
	pass