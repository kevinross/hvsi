#!/usr/bin/env python

import time
from getpass import getpass
from textwrap import TextWrapper

import tweepy, re, urllib
ZOMBIE_SERVER 		= 'hvsi.ca'
ZOMBIE_USER		= 'uoHvsI'
ZOMBIE_PASS		= 'carsonlikesmen'
ZOMBIE_HASH		= ['#hvsi','#HvsI','#Hvsi','#hvsI']
tagre = re.compile(r".*([Hh][A-Za-z0-9]*[Zz]).*")
def tagperson(tagger, id_str, mid):
	print tagger + ' tagged ' + id_str
	fields = tagre.match(id_str)
	if not fields:
		return
	people = fields.groups()
	url = ''.join(['http://',ZOMBIE_SERVER,'/tag/',tagger,'/',people[0],'/',mid])
	login_data = urllib.urlencode(dict(username='zombie_twitter',password='zombie_twitter'))
	d = urllib.urlopen(url, login_data).read()
def update_status(text):
	print 'updating status'
	url = ''.join(['http://',ZOMBIE_SERVER,'/twitter'])
	login_data = urllib.urlencode(dict(username='zombie_twitter',password='zombie_twitter',text=text))
	d = urllib.urlopen(url, login_data).read()
class StreamWatcherListener(tweepy.StreamListener):

	status_wrapper = TextWrapper(width=60, initial_indent='	', subsequent_indent='	')

	def on_status(self, status):
		try:
			print status.user
			print status.text
			if status.user.screen_name==ZOMBIE_USER and status.text[0] != '@':
				update_status(status.text)
			elif [x for x in ZOMBIE_HASH if x in status.text]:
				tagperson(status.user.screen_name, status.text, str(status.id))
		except Exception, e:
			# Catch any unicode errors while printing to console
			# and just ignore them to avoid breaking application.
			print e
	def on_error(self, status_code):
		print 'An error has occured! Status code = %s' % status_code
		return True  # keep stream alive

	def on_timeout(self):
		print 'Snoozing Zzzzzz'

#pyDaemon.createDaemon()
def main():
	global username
	# Prompt for login credentials and setup stream object
	username = ZOMBIE_USER
	password = ZOMBIE_PASS
	stream = tweepy.Stream(username, password, StreamWatcherListener(), timeout=None)

	# Prompt for mode of streaming
	valid_modes = ['sample', 'filter']
	while True:
		mode = 'filter'
		if mode in valid_modes:
			break
		print 'Invalid mode! Try again.'

	if mode == 'sample':
		stream.sample()

	elif mode == 'filter':
		follow_list = ZOMBIE_USER
		track_list = ZOMBIE_HASH
		def convert_screen(screen):
			d = urllib.urlopen("http://api.twitter.com/1/users/show.json?screen_name=" + screen)
			true = True
			false = False
			null = None
			v = d.read()
			d.close()
			info = eval(v)
			return info['id']
		follow_list = [convert_screen(x) for x in follow_list.split(',')]
		while True:
			try:
				stream.filter(follow_list, track_list)
			except:
				time.sleep(10)


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print '\nGoodbye!'

