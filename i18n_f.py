# coding=utf-8
i18n = {
	'name': u'Humains vs Infectés',
	'lang': u'Français',
	'pass': 'Réinitialiser le mot de passe',
	'nav': {
		'home':'Accueil',
		'blog':'Blog',
		'missions':'Missions',
		'party':'Party',
		'register':'Inscription',
		'rules':u'Règlements',
		'stats':'Stats',
		'station':u'Opérations de stations'
	},
	'navd': {
	    'game': 'Jeu'
	},
	'profile': 'Profil',
	'player_status': {
		'state': 'État',
		'active': 'Actif',
		'inactive': 'Inactif',
		'human': 'Humain',
		'zombie': 'Zombie',
		'banned': 'Interdit'
	},
	'pages': {
		'countdown': {
			'title': 'TRANSLATE ME:/pages/page/countdown/title'
		},
		'index': {
			'title': 'Home'
		},
		'login': {
			'title': 'Connecter'
		},
		'blog': {
			'title': 'Blog'
		},
		'thanks': {
			'title': u'Succès',
			'thanks': u"Félicitations, vous êtes maintenant inscrit à HvsI. Nous vous redirigeons à la page d'acceuil..."
		},
		'party': {
			'title': 'Party'
		},
		'missions': {
			'title': 'Missions'
		},
		'rules': {
			'title': u'Règlements'
		},
		'login': {
			'title': 'Connecter',
			'nouser': u"Le nom d'utilisateur que vous avez entré n'existe pas."
		},
		'stats': {
			'title': 'Statistiques',
			'zombiecount24': 'Nombre de Zombies (24 heures)',
			'zombiecountw': 'Nombre de Zombies (semaine)',
			'player': 'Joueurs',
			'time': 'Temps',
			'topzombies': 'Meilleurs tageurs',
			'count': 'Nombre de tags'
		},
		'createedit': {
			'missinginfo': u'Il manque une entrée. Prière de vérifier que toute information nécessaire est fournie.',
			'unknown': u"Une erreur s'est produite, SVP réessayer.",
			'nopostpid': u"L'article demandé n'existe pas.",
			'post_title': 'Titre',
			'post_content': 'Contenu',
			'allow_comments': 'Permettre les commentaires?',
			'cancel': 'Canceller'
		},
		'post_create': {
			'submit': u'Créer',
			'title': u'Créer un article'
		},
		'post_edit': {
			'submit': 'Modifer',
			'title': u"Modifier l'article"
		},
		'register': {
			'title': 'Inscription',
			'name': 'Nom',
			'username': "Nom d'utilisateur",
			'password': 'Mot de passe',
			'password_confirm': 'Confirmation du mot de passe',
			'language': 'Langue',
			'student_num': u'Numéro étudiant',
			'email': 'Courriel',
			'twitter': 'Twitter',
			'cell': 'Céllulaire',
			'gameid': 'ID de jeu',
			'yes': 'Oui',
			'no': 'Non',
			'optional': 'Optionnel',
			'required': 'Requis',
			'register': 'Inscription',
			'userinfo': 'Information du joueur',
			'eula': 'Sécurité et responsabilités',
			'safety': "J'ai lu et j'accepte les",	# format in page: page['safety'] a(text=page['safetyrules'])
			'safetyrules': 'règles de sécurité',
			'liability': "J'ai lu et j'accepte le",# same format
			'liabilitywaiver': 'formulaire de responsabilités',
			'userexists': u"Le nom d'utilisateur que vous avez choisi est déjà pris.",
			'changedlater': u'Peut être changé plus tard.',
			'missinginfo': u'SVP vérifier que toute information nécéssaire est fournie.',
			'wronginfo': 'Information soumise inexacte',
			'noslash': "Aucun slash permis dans le nom d'utilisateur",
			'liability_read': 'Veuiller lire le formulaire de responsabilités',
			'safety_read': 'Veuiller lire les règlements de sécurité',
			'liability_err': 'Vous devez accepter le formulaire de responsabilités afin de joueur',
			'safety_err': 'Vous devez accepter les règlements de sécurité afin de joueur'
		},
		'eula': {
		    'title': 'Sécurité et responsabilités',
		    'agree': "J'accepte"
		},
		'webcheckin': {
			'title': 'Renouvellement en ligne',
			'already': 'Vous avez déjà utilisé votre renouvellement en ligne.',
			'notice': "Vous n'avez qu'un renouvellement en ligne, veuillez confirmer que vous voulez l'utiliser.",
			'confirm': 'Confirmer',
			'notconfirmed': u"Vous n'avez pas cliqué la boîte de confirmation.",
			'soon': u"Cinq heures n'a pas passé depuis votre dernière enregistrement.",
			'human': "Joueur n'est pas un humaine.",
			'kit': u"Joueur n'a pas ramassé son kit.",
			'opererations': "Erreur inconnue."
		},
		'pass_reset': {
			'title': 'Réinitialisation du mot de passe',
			'success': 'Votre mot de passe a été changé à votre numéro étudiant',
			'submit': 'Réinitialiser le mot de passe',
			'wronginfo': 'Incorrect information submitted'
		},
		'station': {
			'title': 'Opérations de station',
			'checkin': {
				'title': 'Renouvellement de joueur',
				'userid': 'ID de jeu',
				'submit': 'Renouveller'
			},
			'cure': {
				'title': 'Guérir Zombie',
				'userid': 'ID de jeu',
				'cureid': 'ID de remède',
				'submit': 'Guérir'
			},
			'tag': {
				'title': 'Enregistrer Tag',
				'taggerid': 'Zombie',
				'taggeeid': 'Victime',
				'submit': 'Tag',
				'game': "Le jeu n'a pas encore commencé"
			},
			'activate': {
				'title': 'Activation de joueur',
				'userid': 'ID du joueur',
				'submit': 'Activer'
			},
			'baduser': "L'utilisateur demandé n'existe pas",
			'game': "Le jeu n'a pas encore commencé",
			'generic': 'Erreur',
			'errors': {
				'notzombie': 'Un joueur doit être un Zombie',
				'nothuman': 'Un joueur doit être un Humain',
				'noplayer': "Aucun joueur avec cette ID existe",
				'nohuman': 'Aucun Humain avec cette ID existe',
				'nozombie': 'Aucun Zombie avec cette ID existe',
				'notstarted': "Le jeu n'a pas encore commencé",
				'kithuman': "L'Humain n'a pas encore ramassé sa trousse",
				'kitzobie': "Le Zombie n'a pas encore ramassé sa trousse",
				'wtf': "Vous n'êtes pas une station mais vous avez des talents de L33T. Comment l'avez-vous fait?: r0ssar00@gmail.com",
				'unknown': 'Erreur inconnue',
				'nouid': 'Aucune ID de jeu donnée',
				'nocid': 'Aucune ID de carte donnée',
				'toosoon': 'Joueur se renouvelle trop tôt',
				'disq': 'La carte remède avec cette ID a été interdite',
				'used': 'La carte remède avec cette ID a déjà été utilisée',
				'activated': 'Le joueur est déjà actif'
			}
		},
		'userlist': {
			'title': 'Utilisateurs',
			'table': {
				'id': 'ID de jeu',
				'username': "Nom d'utilisateur",
				'game_id': 'Game ID',
				'name': 'Nom',
				'status': 'État',
				'signedin': 'Connecté'
			},
			'search_heading': 'Retrieve User',
			'match_on': 'Match via',
			'retrieve': 'Retrieve',
			'nouser': 'No user with the specified %s exists',
			'email': 'email',
			'twitter': 'twitter',
			'cell': 'cell',
			'student_num': 'student number'
		},
		'user_edit': {
			'title': '',
			'editing': 'Modifier',
			'oldpass': 'Ancien mot de passe',
			'userinfo': "Information de l'utilisateur",
			'passchange': 'Modifier le mot de passe',
			'zero': 'Patient Zéro?',
			'makezero': 'Assigner ce joueur Patient Zéro'
		},
		'cures': {
			'title': 'Cartes de remède',
			'table': {
				'id': 'ID de jeu',
				'username': "Nom d'utilisateur",
				'time': 'Heure utilisé',
				'disqualified': 'Disqualifié',
				'disqualify': 'Disqualifier',
				'qualify': 'Qualifier',
				'used': 'Utilisé',
				'cardid': 'ID de remède',
				'delete': 'Supprimer?'
			},
			'addcure': 'Rajouter remède',
			'deletecures': 'Supprimer remèdes'
		},
		'tags': {
			'title': 'Modifier Tags',
			'submit': 'Supprimer Tag(s)',
			'table': {
				'id': 'Tag ID',
				'method': 'Méthode',
				'time': 'Temps',
				'killer': 'Taggeur',
				'victim': 'Victime',
				'delete': 'Supprimer?',
				'cure': 'Guérir la victime?'
			}
		},
		'tag': {
		    'title': 'Enregistrer un tag',
			'tag': 'Tag',
			'unknown': 'Unknown error',
			'duplicate': 'Duplicate found, reload the page and try again'
		},
		'game': {
			'title': 'Contrôle du jeu',
			'start': 'Commencer le jeu',
			'end': 'Terminer le jeu',
			'startr': 'Ouvrir les inscriptions',
			'endr': 'Fermer les inscriptions',
			'encount': 'TRANSLATE ME:/pages/game/encount',
			'discount': 'TRANSLATE ME:/pages/game/discount'
		},
		'editcure': {
			'title': 'Modifier remède',
		},
		'user_view': {
			'title': '',
			'none': 'Aucun',
			'stats': 'Statistiques',
			'kills': 'Tags',
			'deaths': 'Morts',
			'cures': 'Cartes remèdes utilisées',
			'checkin': 'Dernier renouvellement',
			'edit': 'Modifier',
			'activate': 'Activer joueur',
			'kitted': 'Le joueur as-t-il accepté les documents de responsabilité et sécurité? As-t-il reçu son kit?',
			'tags': 'Tags concernant ce joueur',
			'and': 'et'
		},
		'email': {
			'title': 'message générique'
		},
		'http_error': {
			'title': u'Erreur',
			'sorry_part_1': u'Le lien',
			'sorry_part_2': u'cause une erreur.',
			'back': u'Retour'
		}
	},
	'sidebar': {
		'status': {
			'title': u'État',
			'subtitle': '',
			'by': 'par',
			'kills': 'Nombre de tags',
			'humans': 'Humains',
			'zombies': 'Zombies',
			'users': 'Joueurs',
			'used_cures': u'Remèdes utilisés',
			'unused_cures': u'Remèdes non-utilisés',
			'regtag': 'Enregistrer un tag',
			'died': 'Mort',
			'cured': 'Guéri',
			'zero': 'Patient zéro'
		},
		'controls': {
			'title': u'Centre de contrôle',
			'subtitle': '',
			'station': u'Opérations de stations',
			'userlist': "Liste d'utilisateurs",
			'curelist': 'Cartes de remèdes',
			'taglist': 'Tags'
		}
	},
	'post': {
		'edit_post': "Modifier l'article",
		'edit_entry': u'Modifier cette entrée',
		'delete_post': "Supprimer l'article",
		'delete_entry': u"Supprimer cette entrée",
		'permalink': u'Lien permanent à',	# Permanent link to PostName
		'comment': {
			'on': 'Commenter sur',				# Comment on PostName
			'reply': u'Répondre'
		},
		'comment_form': {
			'comments': 'Commentaires',
			'submit': 'Envoyer'
		},
		'nocomments': 'Aucuns commentaires.',
		'postyourcomment': 'Afficher votre commentaire.',
		'cancelreply': u'Cliquez ici pour canceller votre réponse.'
	},
	'loggedinas': u'Connecté en tant que',			# logged in as UserName
	'logoutof': u'Déconnecter',
	'altlang': {
		'key': 'e',
		'name': 'English'
	},
	'days': [
		'Dimanche',
		'Lundi',
		'Mardi',
		'Mercredi',
		'Jeudi',
		'Vendredi',
		'Samedi'
	],
	'email': {
		'subject': 'HvsI: tag automatique',
		'message': u"Vous avex été taguer automatiquement vu que vous n'avez pas deux fois aujourd'hui. S.v.p passer a une station pour echanger votre bandana."
	},
	'logout': u'Déconnecter',
}