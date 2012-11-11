from sqlobject import *
from sqlobject.mysql import builder
from sqlobject.inheritance import *
import bcrypt, datetime, time, markdown, os, urllib, uuid, hashlib
__all__ = ['Game','User','Player','Station','Admin','Tag','Checkin','Cure','Post','Comment','Snapshot','Score','Session', 'Twitter']
NAMESPACE = 'hvsi'
host = 'localhost'
db = 'uottawae_hvsi'
user = 'uottawae_hvsi'
passw = 'hvs.i'
if '_devel' in os.getcwd():
	db = 'hvsi_devel'
	user = 'hvsi'
	passw = 'hvsi'
if 'RDS_HOSTNAME' in os.environ:
	host = os.environ['RDS_HOSTNAME']
	db = os.environ['RDS_DB_NAME']
	user = os.environ['RDS_USERNAME']
	passw = os.environ['RDS_PASSWORD']
sqlhub.processConnection = connectionForURI('mysql://%s:%s@%s/%s' % (user, passw, host, db))
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
class Game(SQLObject):
	class sqlmeta:
		registry = NAMESPACE
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
			return Game.select(Game.q.id == self.i)[0].started
		def __set__(self, obj, value):
			Game.select(Game.q.id == self.i)[0].started = value
			Game.select(Game.q.id == self.i)[0].time = datetime.datetime.now()
	class value_class(object):
		def __init__(self, attr, index):
			self.i = index
			self.attr = attr
		def __get__(self, obj, objtype):
			return getattr(Game.select(Game.q.id == self.i)[0], self.attr)
		def __set__(self, obj, value):
			setattr(Game.select(Game.q.id == self.i)[0], self.attr, value)
	is_started = started_class(1)
	is_reg	   = started_class(2)
	game_start = value_class('time',3)
	game_end   = value_class('time',4)
	game_rego  = value_class('time',5)
	it_email   = value_class('string',6)
	hours_between_checkins = value_class('number',7)
	is_countdown  = started_class(8)
	countdown_time = value_class('time',9)
	@staticmethod
	def toggle_game():
		Game.select(Game.q.id == 1)[0].started = not Game.select(Game.q.id == 1)[0].started
	@staticmethod
	def toggle_reg():
		Game.select(Game.q.id == 2)[0].started = not Game.select(Game.q.id == 2)[0].started
	@staticmethod
	def toggle_countdown():
		Game.select(Game.q.id == 8)[0].started = not Game.select(Game.q.id == 8)[0].started
try:
	Game = Game.select()[0]
except:
	pass

DEFAULT_LIFETIME = 300
class Session(InheritableSQLObject):
	class sqlmeta:
		registry = NAMESPACE
	skey		 = StringCol(length=32,varchar=True,unique=True,notNone=True,default=lambda:uuid.uuid4().get_hex())
	expires		 = DateTimeCol(notNone=True,default=lambda:datetime.datetime.now()+datetime.timedelta(0,DEFAULT_LIFETIME))
	ttl			 = IntCol(default=DEFAULT_LIFETIME)
	language	 = EnumCol(enumValues=['e','f'],default='e')
	user		 = ForeignKey('User',default=None)
	error		 = StringCol(default=None)
	data		 = StringCol(default=None)
	
	@staticmethod
	def grab(key, attr='skey'):
		s = Session.select(getattr(Session.q, attr) == key)[0]
		u = s.user
		if datetime.datetime.now() > s.expires:		# expired
			# destroy and expire it
			s.destroySelf()
			s = Session(user=u)
		s.update_expires()
		return s
		
	def update_expires(self):
		self.expires = datetime.datetime.now() + datetime.timedelta(0, self.ttl)
		
	@staticmethod
	def session(user):
		u = user
		if isinstance(u, basestring):
			u = User.get_user(u)
		if not u:
			return None
		if Session.select(Session.q.user == u).count() == 0:
			s = Session(user=u)
		else:
			s = Session.grab(u, 'user')
		return s
	
class User(InheritableSQLObject):
	class sqlmeta:
		registry = NAMESPACE
	name		 = StringCol(length=50,varchar=True,notNone=True)
	username	 = StringCol(length=25,varchar=True,unique=True,notNone=True)
	hashed_pass	 = StringCol(notNone=True)
	language	 = EnumCol(enumValues=['e','f'],default='e')
	student_num	 = IntCol(unique=True,notNone=True)
	email		 = StringCol(length=50,varchar=True,unique=True,notNone=True)
	twitter		 = StringCol(length=50,varchar=True,unique=True,default=None)
	cell		 = StringCol(length=11,varchar=True,unique=True,default=None)
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
	def _set_cell(self, val):
		self._SO_set_cell(None if not val else norm_cell(val))
	@staticmethod
	def from_id(num):
		try:
			return User.select(User.q.id == num)[0]
		except:
			return None
	@staticmethod
	def from_student_num(num):
		try:
			return User.select(User.q.student_num == num)[0]
		except:
			return None
	@staticmethod
	def from_username(uname):
		try:
			return User.select(User.q.username == uname)[0]
		except:
			return None
	@staticmethod
	def from_twitter(twit):
		if not twit:
			return None
		try:
			return User.select(User.q.twitter == twit)[0]
		except:
			return None
	@staticmethod
	def from_email(email):
		try:
			return User.select(User.q.email == email)[0]
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
			return User.select(User.q.cell == cell)[0]
		except:
			return None
	@staticmethod
	def get_user(v):
		if isinstance(v, User):
			return v
		elif isinstance(v, str):
			return User.from_username(v) or User.from_twitter(v) or User.from_email(v) or User.from_cell(v)
		elif isinstance(v, int):
			# num is large: 12345.  Probably a student number
			if v > 10000:
				return User.from_student_num(v)
			else:
				return User.from_id(v)
locations = ['cby','ucu','cafealt','manual','twitter','email','internet','admin','unset']
states = ['human','zombie','inactive','banned']
class Player(User):
	class sqlmeta:
		registry = NAMESPACE
	state			 = EnumCol(enumValues=states,default='human',notNone=True)
	game_id			 = StringCol(length=10,varchar=True,unique=True,default=None)
	kills			 = SQLMultipleJoin('Tag',joinColumn='tagger_id')
	deaths			 = SQLMultipleJoin('Tag',joinColumn='taggee_id')
	checkins		 = SQLMultipleJoin('Checkin',joinColumn='player_id',orderBy='time')
	cures			 = SQLMultipleJoin('Cure',joinColumn='player_id',orderBy='time')
	signedin		 = BoolCol(default=False,notNone=True)
	signedin_time		 = DateTimeCol(default=None)
	liability		 = BoolCol(default=False)
	safety			 = BoolCol(default=False)
	zero			 = BoolCol(default=False)
	def to_dict(self):
		d = super(Player, self).to_dict()
		d.update(dict(
					state=self.state,
					game_id=self.game_id,
					kills=[x.to_dict() for x in self.kills],
					deaths=[x.to_dict() for x in self.deaths],
					checkins=[x.to_dict() for x in self.checkins],
					cures=[x.to_dict() for x in self.cures],
					signedin=self.signedin,
					signedin_time=self.signedin_time.isoformat()))
		return d
	def _set_zero(self, zero):
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
class Station(User):
	class sqlmeta:
		registry = NAMESPACE
	location		 = EnumCol(enumValues=locations,default='unset',notNone=True)
	def to_dict(self):
		d = super(Station, self).to_dict()
		d['location'] = self.location
		return d
class Admin(User):
	class sqlmeta:
		registry = NAMESPACE
	def _get_location(self):
		return Station.location_admin
	def to_dict(self):
		d = super(Admin, self).to_dict()
		d['location'] = Station.location_admin
		return d
class Tag(SQLObject):
	class sqlmeta:
		registry = NAMESPACE
	time	= DateTimeCol(default=datetime.datetime.now,notNone=True)
	tagger	= ForeignKey('Player',notNone=True)
	taggee  = ForeignKey('Player',notNone=True)
	# prevents spoofing of tags
	uid		= StringCol(length=100,varchar=True,unique=True,notNone=True)
	def to_dict(self):
		return dict(time=self.time.isoformat(), tagger=self.tagger.username, taggee=self.taggee.username, uid=self.uid)
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
class Checkin(SQLObject):
	class sqlmeta:
		registry = NAMESPACE
	time	= DateTimeCol(default=datetime.datetime.now,notNone=True)
	location= EnumCol(enumValues=locations,notNone=True)
	player	= ForeignKey('Player',notNone=True)
	def to_dict(self):
		return dict(time=self.time.isoformat(), location=self.location, player=self.player.username)
class Cure(SQLObject):
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
	def to_dict(self):
		return dict(time=self.time.isoformat(), expiry=self.expiry.isoformat(), card_id=self.card_id, used=self.used, disqualified=self.disqualified, player=self.player.username)
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
class Post(SQLObject):
	class sqlmeta:
		registry = NAMESPACE
	time			= DateTimeCol(default=datetime.datetime.now,notNone=True)
	title_e			= StringCol()
	title_f			= StringCol()
	content_e		= UnicodeCol()
	content_f		= UnicodeCol()
	allow_comments 	= BoolCol(default=True,notNone=True)
	comments		= SQLMultipleJoin('Comment',joinColumn='post_id',orderBy='time')
	def _get_html_e(self):
		return markdown.markdown(self.content_e,output_format='html')
	def _get_html_f(self):
		return markdown.markdown(self.content_f)
	@staticmethod
	def from_pid(pid):
		return Post.select(Post.q.id == pid)[0]
	def to_dict(self):
		return dict(
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
		self.destroySelf()
class Comment(SQLObject):
	class sqlmeta:
		registry = NAMESPACE
	time		= DateTimeCol(default=datetime.datetime.now,notNone=True)
	content		= StringCol()
	user		= ForeignKey('User',notNone=True)
	post		= ForeignKey('Post',notNone=True)
	def _get_html(self):
		return markdown.markdown(self.content, safe_mode="remove")
	def to_dict(self):
		return dict(
			time = self.time.isoformat(),
			content = self.content,
			user = dict(username = self.user.username, name = self.user.name),
			)
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
class Score(SQLObject):
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
class Twitter(SQLObject):
	class sqlmeta:
		registry = NAMESPACE
	time = DateTimeCol(default=datetime.datetime.now)
	query = StringCol()
	content = StringCol(default=None)
	def _set_content(self, new_content):
		self.time = datetime.datetime.now()
		self._SO_set_content(new_content)
	
def set_class_enum(klass, var, array):
	for i in array:
		setattr(klass, var + '_' + i, i)
set_class_enum(Player,'state', states)
set_class_enum(Admin,'location',locations)
set_class_enum(Station,'location',locations)
set_class_enum(Checkin,'location',locations)
def createTables():
	Game.createTable(ifNotExists=True)
	User.createTable(ifNotExists=True)
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
	Twitter.createTable(ifNotExists=True)
createTables()