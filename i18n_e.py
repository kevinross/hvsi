# coding=utf-8
i18n = {
	'name': 'Humans vs Infected',
	'lang': 'English',
	'pass': 'Password Reset',
	'nav': [
		#url	name	display_for_player	display_for_station		display_for_all		display_registration_open
		('home','Home',True,True,True,True),
		('blog','Blog',True,True,True,True),
		('missions','Missions',True,True,True,True),
		('party','Party',True,True,True,True),
		('register','Registration',False,True,True,False),
		('rules','Rules',True,True,True,True),
		('stats','Stats',True,True,True,True),
		('station','Station Operations',False,True,False,True)
	],
	'navd': {
		'game': 'Game'
	},
	'profile': 'User Profile',
	'player_status': {
		'state': 'State',
		'active': 'Active',
		'inactive': 'Inactive',
		'human': 'Human',
		'zombie': 'Zombie',
		'banned': 'Banned'
	},
	'pages': {
		'countdown': {
			'title': 'Countdown / Compte à Rebours'
		},
		'index': {
			'title': 'Home'
		},
		'login': {
			'title': 'Login'
		},
		'blog': {
			'title': 'Blog'
		},
		'thanks': {
			'title': 'Thanks',
			'thanks': 'Thanks for registering, redirecting you back to the main page...'
		},
		'party': {
			'title': 'Party'
		},
		'missions': {
			'title': 'Missions'
		},
		'rules': {
			'title': 'Rules'
		},
		'login': {
			'title': 'Login',
			'nouser': 'No such user or incorrect password'
		},
		'stats': {
			'title': 'Statistics',
			'zombiecount24': 'Zombie Count (24 hours)',
			'zombiecountw': 'Zombie Count (Week)',
			'player': 'Players',
			'time': 'Time',
			'topzombies': 'Top Zombies',
			'count': 'Count'
		},
		'createedit': {
			'missinginfo': 'Missing a field, make sure all fields have beein submitted.',
			'unknown': 'Unknown error occured, please try again.',
			'nopostpid': "A post with this ID doesn't exist.",
			'post_title': 'Title',
			'post_content': 'Content',
			'allow_comments': 'Allow Comments?',
			'cancel': 'Cancel'
		},
		'post_create': {
			'submit': 'Create',
			'title': 'Create Post'
		},
		'post_edit': {
			'submit': 'Edit',
			'title': 'Edit Post'
		},
		'game': {
			'title': 'Game Control',
			'start': 'Start Game',
			'end': 'End Game',
			'startr': 'Open Registrations',
			'endr': 'Close Registrations',
			'encount': 'Enable Countdown',
			'discount': 'Disable Countdown'
		},
		'register': {
			'title': 'Registration',
			'name': 'Name (first and last)',
			'username': 'Username',
			'password': 'Password',
			'password_confirm': 'Password (confirm)',
			'language': 'Language',
			'student_num': 'Student Number',
			'email': 'Email',
			'twitter': 'Twitter',
			'cell': 'Cell Number',
			'gameid': 'Game ID',
			'yes': 'Yes',
			'no': 'No',
			'optional': 'Optional',
			'required': 'Required',
			'register': 'Register',
			'userinfo': 'Player Information',
			'eula': 'Safety and Liability',
			'safety': 'I have read and accepted the',	# format in page: page['safety'] a(text=page['safetyrules'])
			'safetyrules': 'safety rules',
			'liability': 'I have read and accepted the',# same format
			'liabilitywaiver': 'liability waiver',
			'userexists': 'User already registered.',
			'changedlater': 'Can be changed later',
			'missinginfo': 'Please make sure all required fields are filled in',
			'wronginfo': 'Incorrect information submitted',
			'noslash': 'No slashes are permitted in usernames',
			'liability_read': 'The liability waiver has not been read',
			'safety_read': 'The safety rules have not been read',
			'liability_err': 'You may not register unless you agree to the terms in the liability waiver',
			'safety_err': 'You may not register unless you agree to the safety rules'
		},
		'eula': {
			'title': 'Safety and Liability',
			'agree': 'Agree'
		},
		'webcheckin': {
			'title': 'Web Checkin',
			'already': 'You have already used your web checkin.',
			'notice': 'You have one web checkin, select the checkbox and click "Web Checkin" to use it.',
			'confirm': 'Confirm',
			'notconfirmed': 'You did not click the "Confirm" checkbox.',
			'soon': 'Your last check-in was less than 5 hours ago.',
			'human': 'Player is not a human.',
			'kit': 'Player has not picked up kit',
			'opererations': 'Unknown error'
		},
		'pass_reset': {
			'title': 'Password Reset',
			'success': 'Your password has been reset to your student number',
			'submit': 'Reset password'
		},
		'station': {
			'title': 'Station Operations',
			'checkin': {
				'title': 'Player Checkin',
				'userid': 'User ID',
				'submit': 'Checkin'
			},
			'cure': {
				'title': 'Cure Zombie',
				'userid': 'User ID',
				'cureid': 'Cure Card ID',
				'submit': 'Cure'
			},
			'tag': {
				'title': 'Register Tag',
				'taggerid': 'Zombie',
				'taggeeid': 'Victim',
				'submit': 'Tag',
				'game': 'Game not started'
			},
			'activate': {
				'title': 'Player Activation',
				'userid': 'User ID',
				'submit': 'Activate'
			},
			'baduser': 'No such user(s)',
			'game': 'Game not started',
			'generic': 'Error',
			'errors': {
				'notzombie': 'A player must be a zombie',
				'nothuman': 'A player must be a human',
				'noplayer': 'No player with that ID exists',
				'nohuman': 'No human with that ID exists',
				'nozombie': 'No zombie with that ID exists',
				'notstarted': 'Game not started',
				'kithuman': 'Human has not picked up kit',
				'kitzobie': 'Zombie has not picked up kit',
				'wtf': 'You are not a station and yet you managed to get this far.  Congratulations, now email me how you did it: r0ssar00@gmail.com',
				'unknown': 'Unknown error',
				'nouid': 'No user ID given',
				'nocid': 'No card ID given',
				'toosoon': 'Player checking in too soon',
				'disq': 'Cure card with this ID was disqualified',
				'used': 'Cure card with this ID was already used',
				'activated': 'Player has already been activated'
			}
		},
		'userlist': {
			'title': 'Users',
			'table': {
				'id': 'ID',
				'username': 'Username',
				'name': 'Name',
				'status': 'Status',
				'signedin': 'Active'
			}
		},
		'useredit': {
			'title': '',
			'editing': 'Editing',
			'oldpass': 'Old Password',
			'userinfo': 'Basic User Data',
			'passchange': 'Change Password',
			'zero': 'Patient Zero?',
			'makezero': 'Make this player Patient Zero'
		},
		'cures': {
			'title': 'Cure Cards',
			'table': {
				'id': 'ID',
				'username': 'Username',
				'time': 'Time Used',
				'disqualified': 'Disqualified',
				'disqualify': 'Disqualify',
				'qualify': 'Qualify',
				'used': 'Used',
				'cardid': 'Card ID',
				'delete': 'Delete?'
			},
			'addcure': 'Add Cure',
			'deletecures': 'Delete Cures'
		},
		'editcure': {
			'title': 'Edit Cure',
		},
		'tags': {
			'title': 'Edit Tags',
			'submit': 'Delete Tag(s)',
			'table': {
				'id': 'Tag ID',
				'method': 'Report Method',
				'time': 'Time',
				'killer': 'Tagger',
				'victim': 'Victim',
				'delete': 'Delete?',
				'cure': 'Cure Victim?'
			}
		},
		'tag': {
			'title': 'Register A Tag',
			'tag': 'Tag'
		},
		'email': {
			'title': 'Mass Email'
		},
		'user': {
			'title': '',
			'none': 'None',
			'stats': 'Statistics',
			'kills': 'Tags',
			'deaths': 'Deaths',
			'cures': '# Used cure cards',
			'checkin': 'Last checkin',
			'edit': 'Edit',
			'activate': 'Activate Player',
			'kitted': 'Player has accepted liability + safety rules and has received kit?',
			'tags': 'Tags involving this player',
			'and': 'and'
		},
		'http_error': {
			'title': 'Error',
			'sorry_part_1': 'Sorry, the requested URL',
			'sorry_part_2': 'caused an error',
			'back': 'Back'
		}
	},
	'sidebar': {
		'status': {
			'title': 'Status',
			'subtitle': '',
			'by': 'by',
			'kills': 'Tags',
			'humans': 'Humans',
			'zombies': 'Zombies',
			'users': 'Players',
			'used_cures': 'Used Cures',
			'unused_cures': 'Unused Cures',
			'regtag': 'Register a Tag',
			'died': 'Died',
			'cured': 'Cured',
			'zero': 'Patient Zero'
		},
		'controls': {
			'title': 'Control Panel',
			'subtitle': '',
			'station': 'Station Operations',
			'userlist': 'User List',
			'curelist': 'Cure Cards',
			'taglist': 'Tags'
		}
	},
	'post': {
		'edit_post': 'Edit post',
		'edit_entry': 'Edit this entry',
		'delete_post': 'Delete post',
		'delete_entry': 'Delete this entry',
		'permalink': 'Permanent link to',	# Permanent link to PostName
		'comment': {
			'on': 'Comment on',				# Comment on PostName
			'reply': 'Reply'
		},
		'comment_form': {
			'comments': 'Comments',
			'submit': 'Submit'
		},
		'nocomments': 'No comments yet',
		'postyourcomment': 'Post your comments',
		'cancelreply': 'Click here to cancel reply.'
	},
	'loggedinas': 'Logged in as',			# logged in as UserName
	'logoutof': 'Log out of this account',
	'altlang': {
		'key': 'f',
		'name': u'Français'
	},
	'days': [
		'Sunday',
		'Monday',
		'Tuesday',
		'Wednesday',
		'Thursday',
		'Friday',
		'Saturday'
	],
	'email': {
		'subject': 'HvsI: Auto-tag',
		'message': 'You have been auto-tagged because you did not check-in twice today.\nPlease stop by a station and exchange your bandanna.'
	},
	'logout': 'Logout',
}
