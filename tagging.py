from database import *
__all__ = ['add_kill']
class TagException(Exception):
	pass
def add_kill(tagger, taggee, uid):
	tagger = Player.from_game_id(tagger) or Player.from_twitter(tagger) or Player.from_email(tagger) or Player.from_cell(tagger)
	if tagger.state != Player.state_zombie:
		raise TagException(tagger.username + ' is not a zombie')
	taggee = Player.from_game_id(taggee)
	if taggee.state != Player.state_human:
		raise TagException(taggee.username + ' is not a human')
	if Tag.has_uid(uid):
		raise TagException(uid + ' already exists, ' + tagger.username + ' may be attempting to cheat')
	return Tag(tagger=tagger,taggee=taggee,uid=uid)