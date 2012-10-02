from database import *
import datetime
__all__ = ['TagException','CheckInException','CureException','add_kill','do_checkin','do_cure','EXC_NOTHUMAN','EXC_NOTZOMBIE','EXC_KITHUMAN','EXC_KITZOMBIE','EXC_NOTSTATION','EXC_NOSUCHZOMBIE','EXC_NOSUCHHUMAN','CHECKIN_TOOSOON','CURE_DISQUALIFIED','CURE_ALREADYUSED']
EXC_NOTHUMAN = 'player is not a human'
EXC_NOTZOMBIE= 'player is not a zombie'
EXC_KITHUMAN = 'human has no kit'
EXC_KITZOMBIE= 'zombie has no kit'
EXC_NOTSTATION='non-station attempting to perform station operations'
EXC_NOSUCHZOMBIE='no such zombie exists'
EXC_NOSUCHHUMAN='no such human exists'
CHECKIN_TOOSOON = 'player checked in too soon'
CURE_DISQUALIFIED = 'cure card is disqualified'
CURE_ALREADYUSED = 'cure card already used'
class TagException(Exception):
	pass
class CheckInException(Exception):
	pass
class CureException(Exception):
	pass
def add_kill(tagger, taggee, uid, override=False):
	"""
	Parameters:
		tagger: Player inst, game_id, email, student num, twitter, or cell number
		taggee: game_id
		uid: uniquely identifying string.  can be the Message-ID from email, tweet id, uuid, etc.
	Returns:
		Tag instance
	Throws:
		TagException
	"""
	v = uid
	if isinstance(tagger, str) and '@' in tagger:
		try:
			i = int(tagger[:tagger.find('@')])
			if len(str(i)) >= 10:
				v = 'cell_' + uid
		except:
			pass
#	print 'passed: ' + str(taggee)
	tagger = Player.get_player(tagger)
	if not override:
		taggee = Player.from_game_id(taggee)
#	print 'found: ' + str(taggee)
	if override:
		if not isinstance(taggee, Player):
			taggee = Player.get_player(taggee)
#	print taggee
	if not tagger:
		raise TagException(EXC_NOSUCHZOMBIE)
	if not taggee:
		raise TagException(EXC_NOSUCHHUMAN)
	if Tag.has_uid(uid):
		raise TagException(uid + ' already exists, ' + tagger.username + ' may be attempting to cheat')
	if not tagger.is_zombie():
		tagger.kill()
	if not taggee.is_human() and not override:
		raise TagException(EXC_NOTHUMAN)
	if not tagger.signedin and not override:
		raise TagException(EXC_KITZOMBIE)
	if not taggee.signedin and not override:
		raise TagException(EXC_KITHUMAN)
	taggee.kill()
	t = Tag(tagger=tagger,taggee=taggee,uid=v)
	# update scorecard
	Score.get_scorecard(tagger).kills = tagger.kills.count()
	return t
def do_checkin(player, station):
	"""
	Parameters:
		player: Player inst, game_id, email, student num, twitter, or cell number
		station: Station inst
	Returns:
		Checkin instance
	Throws:
		CheckinException
	"""
	player = Player.get_player(player)
	if not player:
		raise CheckInException(EXC_NOSUCHHUMAN)
	if not (isinstance(station, Station) or isinstance(station, Admin)):
		raise CheckInException(EXC_NOTSTATION)
	if player.last_checkin_time:
		if datetime.datetime.now() < player.last_checkin_time + datetime.timedelta(0,0,0,0,0,Game.hours_between_checkins):
			raise CheckInException(CHECKIN_TOOSOON)
	if not player.is_human():
		raise CheckInException(EXC_NOTHUMAN)
	if not player.signedin:
		raise CheckInException(EXC_KITHUMAN)
	return Checkin(location=station.location,player=player)
def do_cure(player, station, cure):
	"""
	Parameters:
		player: Player inst, game_id, email, student num, twitter, or cell number
		station: station inst
		cure: Cure inst or id
	Returns:
		Whether the cure succeeded
	Throws:
		CureException
	"""
	player = Player.get_player(player)
	if not player:
		raise CheckInException(EXC_NOSUCHZOMBIE)
	if not (isinstance(station, Station) or isinstance(station, Admin)):
		raise CureException(EXC_NOTSTATION)
	if not player.is_zombie():
		raise CureException(EXC_NOTZOMBIE)
	if not player.signedin:
		raise CureException(EXC_KITZOMBIE)
	cure = Cure.get_cure(cure)
	if cure.disqualified:
		raise CureException(CURE_DISQUALIFIED)
	if cure.used:
		raise CureException(CURE_ALREADYUSED)
	cure.time = datetime.datetime.now()
	cure.used = True
	cure.player = player
	player.cure()
	return True
