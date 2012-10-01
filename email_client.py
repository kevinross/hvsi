#!/usr/bin/env python
"""
So, you're confused as to why you can get email PUSHed to your mobile phone (iPhone, for example, 
but there are others, of course) or your iPod Touch (in my case) but not your computer (mac, in 
this case). I've got the Google notifier, but that checks the server, by default, every 15 mins (if 
my memory serves me correctly. I've changed that to 5 mins using the hidden preference thing (google
'gmail notifier interval' to find it) but that makes me feel a little rude. IMAP PUSH is the answer,
but the notifiers don't seem to use it. 

This script wasn't written as a replacement for the gmail notifier, but i'll certainly work on it. 
The idea behind this script was to allow for easy modification to use in your projects by looking
at this fairly complete script. If you want it to do something different, you could change the 
self.showNewMailMessages() line in waitForServer() to whatever you want. Perhaps you've got an
Arduino and you want it to light something up as soon as (well about 3-4 seconds later) the message
is sent. A fairly simple example, i know, but you get the idea.

For this script to work, you need to enable IMAP in the GMail settings. Just to make sure you got
that:

			!!! ENABLE IMAP IN YOUR GMAIL SETTINGS !!!

"""



"""
Released under the MIT/X11 License

Copyright (c) 2010 -- Chris Kirkham

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.
"""

__version__ = '0.1'
__author__  = 'Chris Kirkham'
__URL__	    = 'http://hmmtheresanidea.blogspot.com'
__credits__ = """
	* Tim's Weblog - http://blog.hokkertjes.nl/2009/03/11/python-imap-idle-with-imaplib2/ - 
	this was a great help. It got me on the right track. It taught me the Event() stuff as 
	well, so that was good.

	* Piers Lauder - http://www.cs.usyd.edu.au/~piers/python/imaplib.html - for imaplib2 
	and the documentation alongside it. Couldn't have done it without him! Thanks!
	
	* Kevin Ross - modified to work with HvsI
"""
__license__ = "MIT/X11"
__version__ = "1.0.1"


import threading, imaplib2, os, sys, getpass, email, urllib, re, time

ZOMBIE_USER		= 'tag@hvsi.ca'
ZOMBIE_PASS		= 'P@s5w0rD'
ZOMBIE_SERVER 		= 'hvsi.ca'

ServerTimeout	  = 29 # Mins   		(leave if you're not sure)

# This is where the magic happens. Change the code below at your peril!
# Obviously if you know what you're doing, or just want to fiddle, go ahead. Don't let this warning stop you!
# But, as it is, this should work. As before, make sure you have IMAP enabled.

#'True' to enter debug mode
DEBUG = True # debugMsg() prints the parameter passed if DEBUG is True

tagre = re.compile(r".*([Hh][A-Za-z0-9]*[Zz]).*")
"""
The worker class for the thread. Letting a thread wait for the server to send something allows the
main thread (if that's what you call it??) to be used for other stuff -- waiting for UI, for example.
"""
class Idler(threading.Thread):
		
	imap = imaplib2.IMAP4_SSL("imap.gmail.com") # can be changed to another server if needed
	
	stopWaitingEvent = threading.Event()
	#Now, this stopWaitingEvent thing -- it really does make the whole thing work. Basically, 
	#it holds a boolean value which is set and cleared using, oddly enough, the methods set() and
	#clear(). But, the good thing about it is that it has another method, wait(), which holds 
	#execution until it has been set(). I cannot thank threading.Event() enough, I really couldn't
	#have done it without you!
	
	knownAboutMail = [] # will be a list of IDs of messages in the inbox
	killNow = False # stops execution of thread to allow propper closing of conns.
	
	
	"""
	Initialise (sorry, I'm from the UK) everything to get ready for PUSHed mail.
	"""
	def __init__(self, GMailUsername, GMailPassword):
		
#		os.system('clear')
		debugMsg('DEBUG is ENABLED')
		debugMsg('__init__() entered')
				
		try:
			#establish connection to IMAP Server
			self.imap.LOGIN(GMailUsername, GMailPassword)
			self.imap.SELECT("INBOX")
			
			#get the IDs of all messages in the inbox and put in knowAboutMail
			typ, data = self.imap.SEARCH(None, 'ALL')
			self.knownAboutMail = data[0].split()
			
			#now run the inherited __init__ method to create thread
			threading.Thread.__init__(self)
			
		except Exception, e: #Uh Oh, something went wrong
			print 'ERROR: IMAP Issue. It could be one (or more) of the following:'
			print '- The impalib2.py file needs to be in the same directory as this file'
			print '- You\'re not connected to the internet'
			print '- Google\'s mail server(s) is/are down'
			print '- Your username and/or password is incorrect'
			print e.message
			sys.exit(1)
			
		debugMsg('__init__() exited')
		
		
	"""
	The method invoked when the thread id start()ed. Enter a loop executing waitForServer()
	untill kill()ed. waitForServer() can, and should, be continuously executed to be alerted
	of new mail.
	"""
	def run(self):
		debugMsg('run() entered')	
		
		#loop until killNow is set by kill() method
		while not self.killNow:
			self.waitForServer()	
			
		debugMsg('run() exited')
			
	
	"""
	If growlnotify is installed, use it; if not, just use regular old print. If you don't have 
	growl notify, you can get it from the .dmg you downloaded for growl. It's in there!
	"""
	def growlnotify(self, title, message):
		debugMsg('growlnotify() entered')
		
		#if growlnotify is installed, show notification
		if os.path.isfile('/usr/local/bin/growlnotify'):
			
			#The command string - os.system()ed to use growlnotify
			#set --appIcon as the .app that you want the icon to be. I used the Google Notifier icon
			cmd = " ".join(["growlnotify", '"'+title+'"', "-m", '"'+message+'"', '--appIcon "/Volumes/OSX/Applications/Google Notifier.app"'])
			
			debugMsg('growlnotify cmd string:')
			debugMsg(cmd, 0)
			os.system(cmd)
		
		#if not, just print it out
		else:
			debugMsg('WARNING: growlnotify not installed. See http://growl.info/extras.php#growlnotify for info on how to get it.')
			print ' '
			print 'NEW MAIL:'
			print '--', title
			print '--', message
		
		debugMsg('growlnotify() exited')

	def tagperson(self, tagger, id_str, mid):
		debugMsg('tagperson() entered: ' + tagger + ',' + id_str + ',' + mid)
		fields = tagre.match(id_str)
		if not fields:
			return
		people = fields.groups()
		url = ''.join(['http://',ZOMBIE_SERVER,'/tag/',tagger,'/',people[0],'/',urllib.urlencode(dict(_=mid))[2:]])
		login_data = urllib.urlencode(dict(username='zombie_email',password='zombie_pass'))
		d = urllib.urlopen(url, login_data).read()	
		debugMsg('tagperson() exited')

	"""
	Name says it all really: get (just) the specified header fields from the server for the 
	specified message ID.
	"""
	def getMessageHeaderFieldsById(self, id, fields_tuple):
		debugMsg('getMessageHeaderFieldsById() entered')
		
		#get the entire header
		typ, header = self.imap.FETCH(id, '(BODY.PEEK[HEADER])')
		#get individual lines
		msg = email.message_from_string(header[0][1])
		
		#get the lines that start with the values in fields_tuple
		results = {}
		for field in fields_tuple:
			results[field] = ''
			for line in msg.keys():
				if line.startswith(field):
					results[field] = msg[line]
					
		debugMsg('getMessageHeaderFieldsById() exited')
		return results #which is a dictionary containing the the requested fields
	
	def getBodyById(self, id):
		debugMsg('getBodyById() entered')
		typ, body = self.imap.FETCH(id, '(BODY.PEEK[TEXT])')
		b = body[0][1]
		if len(b) > 2:
			while b[-1] == '\r' or b[-1] == '\n':
				b = b[0:len(b)-2]
		debugMsg('getBodyById() exited')
		return b
	
	def markIdAsRead(self, id):
		debugMsg('markIdAsRead() entered')
		_ = self.imap.FETCH(id, '(RFC822)')
		debugMsg('markIdAsRead() exited')

	"""
	The main def for displaying messages. It draws on getMessageHeaderFieldsById() and growlnotify()
	to do so.
	"""
	def showNewMailMessages(self):
		debugMsg('showNewMailMessages() entered')
		
		#get IDs of all UNSEEN messages 
		typ, data = self.imap.SEARCH(None, 'UNSEEN')
		
		debugMsg('data - new mail IDs:')
		debugMsg(data, 0)
		
		for id in data[0].split():
				
			#get From and Subject fields from header
			headerFields = self.getMessageHeaderFieldsById(id, ('From', 'Subject', 'Message-ID'))
			body = self.getBodyById(id).replace('\n','').replace('\r','')
			self.markIdAsRead(id)
				
			debugMsg('headerFields dict. (from showNewMailMessage()):')
			debugMsg(headerFields, 0)
			debugMsg('body (from showNewMailMessage()):')
			debugMsg(body)
			from_ = headerFields['From']
			if '<' in from_:
				from_ = from_[from_.find('<')+1:]
				from_ = from_[:from_.find('>')]
			self.tagperson(from_,headerFields['Subject'], headerFields['Message-ID'])
			# self.growlnotify(" ".join(['Mail', headerFields['From']]), "'"+headerFields['Subject']+"'")
			
			#add this message to the list of known messages
			self.knownAboutMail.append(id)
				
		debugMsg('showNewMailMessages() exited')


	"""
	Called to stop the script. It stops the continuous while loop in run() and therefore
	stops the thread's execution.
	"""
	def kill(self):
		self.killNow = True # to stop while loop in run()
		self.timeout = True # keeps waitForServer() nice
		self.stopWaitingEvent.set() # to let wait() to return and let execution continue


	"""
	This is the block of code called by the run() method of the therad. It is what does all 
	the waiting for new mail (well, and timeouts).
	"""
	def waitForServer(self):
		debugMsg('waitForServer() entered')
		
		#init
		self.newMail = False
		self.timeout = False
		self.IDLEArgs = ''
		self.stopWaitingEvent.clear()
		
		def _IDLECallback(args):
			self.IDLEArgs = args
			self.stopWaitingEvent.set()
			#_IDLECallack() is entered when the IMAP server responds to the IDLE command when new
			#mail is received. The self.stopWaitingEvent.set() allows the .wait() to return and
			#therefore the rest of waitForServer().
			
			
		#attach callback function, and let server know it should tell us when new mail arrives	
		self.imap.idle(timeout=60*ServerTimeout, callback=_IDLECallback)

		#execution will stay here until either:
		# - a new message is received; or
		# - the timeout has happened 
		#   	- we set the timout -- the RFC says the server has the right to forget about 
		#	  	  us after 30 mins of inactivity (i.e. not communicating with server for 30 mins). 
		#	  	  By sending the IDLE command every 29 mins, we won't be forgotten.
		# - Alternatively, the kill() method has been invoked.
		self.stopWaitingEvent.wait()
		
		#self.IDLEArgs has now been filled (if not kill()ed)
		
		if not self.killNow: # skips a chunk of code to sys.exit() more quickly.
			
			if self.IDLEArgs[0][1][0] == ('IDLE terminated (Success)'):
			# This (above) is sent when either: there has been a timeout (server sends); or, there
			# is new mail. We have to check manually to see if there is new mail. 
				
				typ, data = self.imap.SEARCH(None, 'UNSEEN') # like before, get UNSEEN message IDs
				
				debugMsg('Data: ')
				debugMsg(data, 0)
				
				#see if each ID is new, and, if it is, make newMail True
				for id in data[0].split():
					print id
					print self.knownAboutMail
					self.newMail = self.newMail or True
					# let's not give a FUCK about old email, it *will* get marked read by the daemon
#					if not id in self.knownAboutMail:
#						self.newMail = self.newMail or True
#					else:
#						self.timeout = True 
						# gets executed if there are UNSEEN messages that we have been notified of, 
						# but we haven't yet read. In this case, it response was just a timeout.
						
				if data[0] == '': # no IDs, so it was a timeout (but no notified but UNSEEN mail)
					print 'timeout'
					self.timeout = True
		
			#now there has either been a timeout or a new message -- Do something...
			if self.newMail:
				debugMsg('INFO: New Mail Received')
				self.showNewMailMessages()
							
			elif self.timeout:
				debugMsg('INFO: A Timeout Occurred')
			
		debugMsg('waitForServer() exited')
			
			

"""
Simple procedure to output debug messages nicely.
"""
def debugMsg(msg, newline=1):
	global DEBUG
	if DEBUG:
		if newline:
			print ' '
		print msg
	
#import pyDaemon	
#pyDaemon.createDaemon()
"""
Main bit of code to get the ball rolling. It starts the thread and waits for 'q' to be input.
That's it. Nice and simple.
"""
def main():
	global ZOMBIE_USER
	global ZOMBIE_PASS
	print 'starting up...'
	idler = Idler(ZOMBIE_USER, ZOMBIE_PASS)
	print 'made idler...'
	idler.start()
	
	print '* Waiting for mail...'
	q = ''
	while True:
		time.sleep(10)
		
	idler.kill()	
	idler.imap.CLOSE()
	idler.imap.LOGOUT()
	sys.exit()



if __name__ == '__main__': # then this script is being run on its own, i.e. not imported
	main()
else:
	print 'I don\'t think you ment to import this'
	sys.exit(1)
	
