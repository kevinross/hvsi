import os, sys, random, string, datetime, time
from sqlobject import *
from database import *
import i18n
import smtplib
from email.mime.text import MIMEText
from email.Header import Header
os.environ['TZ'] = 'America/Toronto'
time.tzset()

if len(sys.argv) > 1:
	real = True
else:
	real = False
from database import *
from ops import *

s = smtplib.SMTP_SSL('localhost',465)
s.login('hvsi@hvsi.ca',"HvsI_email_sender")

bot = Player.from_username('military.militaire')
today = datetime.datetime.now()
eight30 = datetime.datetime(today.year, today.month, today.day, 8, 00, 0, 0)
four30 = datetime.datetime(today.year, today.month, today.day, 23, 55, 00, 0)

monday = datetime.datetime(Game.game_start.year, Game.game_start.month, Game.game_start.day, 12, 30, 0, 0)
tuesday = datetime.datetime(Game.game_start.year, Game.game_start.month, Game.game_start.day+1, 12, 30, 0, 0)
tuesday_four30 = datetime.datetime(Game.game_start.year, Game.game_start.month, Game.game_start.day+1, 22, 30, 0, 0)
def inform_player(players):
	subject = i18n.i18n['e']['email']['subject'] + '/' + i18n.i18n['f']['email']['subject']
	subject = Header(unicode(subject), 'utf-8')
	body = i18n.i18n['e']['email']['message'] + '\n\n\n' + i18n.i18n['f']['email']['message']
	msg = MIMEText(body.encode('utf-8'), 'plain', 'utf-8')
	msg['From'] = 'tag@hvsi.ca'
	msg['Subject'] = subject
	if real:
		s.sendmail(msg['From'], [x.email for x in players], msg.as_string())
def check_player(player):
	uid = "bot_" + ''.join(random.sample(string.ascii_letters+string.digits, 36))
	# today's checkins < 2
	todays = player.checkins.filter(AND(Checkin.q.time <= four30,Checkin.q.time >= eight30))
	print 'Checking %s, checkins today: %i' % (player.username, todays.count())
	if todays.count() < 2:
		if todays.count() > 0:
			for i in todays:
				print '	' + i.time.strftime('%b %d @ %H:%M')
		if today <= tuesday_four30:
			if player.signedin_time:
				print '	Signedin:' + player.signedin_time.strftime('%b %d @ %H:%M')
			if player.signedin and player.signedin_time and player.signedin_time.date() == monday.date():
				if player.signedin_time > monday:
					return False
			elif player.signedin and player.signedin_time and player.signedin_time.date() == tuesday.date():
				if player.signedin_time > tuesday:
					return False
		elif player.signedin and not player.signedin_time:
			return False
		print "killing " + player.username + ', with checkin count ' + str(todays.count())
		for i in player.checkins:
			print '	checkin:' + i.time.isoformat()
		for i in player.kills:
			print ' killed %s @ %s' % (i.taggee.username, time.isoformat())
		if real:
			add_kill(bot, player, uid, override=True)
		return player
		
if __name__ == '__main__':
	players = Player.humans
	informs = [x for x in [check_player(y) for y in players] if x]
	inform_player(informs)
s.quit()
