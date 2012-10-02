# ************************************************************
# Sequel Pro SQL dump
# Version 3408
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: localhost (MySQL 5.5.28)
# Database: hvsi_devel
# Generation Time: 2012-10-02 19:09:56 -0400
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table admin
# ------------------------------------------------------------

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;

INSERT INTO `admin` (`id`, `child_name`)
VALUES
	(1,NULL);

/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table checkin
# ------------------------------------------------------------



# Dump of table comment
# ------------------------------------------------------------



# Dump of table cure
# ------------------------------------------------------------



# Dump of table game
# ------------------------------------------------------------

LOCK TABLES `game` WRITE;
/*!40000 ALTER TABLE `game` DISABLE KEYS */;

INSERT INTO `game` (`id`, `started`, `time`, `string`, `number`)
VALUES
	(1,0,'2012-10-02 13:56:18',NULL,NULL),
	(2,1,'2012-10-02 13:56:23',NULL,NULL),
	(3,0,'2010-11-10 21:12:34',NULL,NULL),
	(4,0,'2012-10-03 00:00:00',NULL,NULL),
	(5,0,'2012-10-04 19:36:34',NULL,NULL),
	(6,NULL,NULL,'it@hvsi.ca',NULL),
	(7,NULL,NULL,NULL,4);

/*!40000 ALTER TABLE `game` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table player
# ------------------------------------------------------------



# Dump of table post
# ------------------------------------------------------------

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;

INSERT INTO `post` (`id`, `time`, `title_e`, `title_f`, `content_e`, `content_f`, `allow_comments`)
VALUES
	(1,'2010-10-10 10:10:10','Home','Accueil','##What is HvsI?##\r\nHumans vs Infected is a week-long game of zombie-themed tag played at the University of Ottawa. Go to [Missions](/missions) for the week\'s schedule and **prizes to be won**. Go to [Rules](/rules) to learn how to play.\r\n\r\n##How to Register?##\r\n[Register online now](/register) or at a registration table (CBY or CafÃ© Alt) on Nov 1 or 2. The game runs from Monday @9AM to Friday @8PM. You still need to pick up your kit before you can start playing.\r\n\r\n##Cost?##\r\n###Registration and kits are FREE!###\r\n5$ late fee on Tuesday.\r\n\r\n###T-shirts are 5$.###\r\nKits and t-shirts available at CafÃ© Alt or CBY. Kits only on Monday and Tuesday.\r\n\r\nThe earlier you pick up your kit, the more bracelets you get to protect yourself. 6 bracelets Monday before 1PM, 4 Monday after 1PM, 2 Tuesday.\r\n\r\nEmail [president@hvsi.ca](mailto:president@hvsi.ca) if you have any questions.','##C\'est quoi HvsI?##\r\nHumains vs InfectÃ©s est un jeu de tag-zombie jouÃ© Ã  l\'UniversitÃ© d\'Ottawa. Allez Ã  [Missions](/missions) pour l\'horaire des Ã©vÃ©nements et les **prix Ã  gagner**. Allez Ã  [RÃ¨glements](/rules) pour apprendre Ã  jouer.\r\n\r\n##Comment S\'inscrire?##\r\n[Inscription en ligne dÃ¨s maintenant](/register) ou Ã  une table d\'enregistrement (CBY ou CafÃ© Alt) le 1 ou 2 novembre. HvsI est en jeu du lundi Ã  9h au vendredi Ã  20h. Vous devez obtenir votre trousse avant de commencer Ã  jouer.\r\n\r\n##CoÃ»t?##\r\n###Inscription et trousses GRATUITE!###\r\nFrais de retard de 5$ le mardi.\r\n\r\n###T-shirts sont 5$.###\r\nTrousses et t-shirts disponibles au CafÃ© Alt et Ã  CBY. Trousses seulement lundi et mardi.\r\n\r\nLe plus tÃ´t que vous ramassez votre kit, le plus de bracelets vous obtenez. 6 bracelets lundi avant 13h, 4 lundi aprÃ¨s 13h, 2 mardi.\r\n\r\nContactez-nous Ã  [president@hvsi.ca](mailto:president@hvsi.ca) si vous avez des questions.',0),
	(2,'2010-10-20 13:46:49','Missions and Prizes','Missions et prix','## General Missions\r\n**Last Human Alive:** Survive the week and win the Ultimate Challenge and win a __PlayStation 3.__\r\n\r\n**Most Tags:** Tag the most number of Humans and win an __XBOX 360.__\r\n\r\n**Best Recorded Tag:** The best tag video gets you an __iPod Touch.__\r\n\r\n**Most Socks:** Collect the most HvsI sock bracelets and win an __iPod Nano.__\r\n\r\n**Bounties:** Several campus celebrities, whose names we will release when the time is right, have had bounties placed on their heads. Tag a celebrity and win a __50$ gift certificate at EB Games.__\r\n\r\n**Picture List:** Take pictures of yourself in your HvsI t-shirt [all around Ottawa](/pdf/photo_list_e.pdf). The person with the most points wins a __100$ tab at CafÃ© Nostalgica.__\r\n\r\n**Farthest Tag:** Tag a Human the farthest from campus and each of you wins a __50$ tab at 1848.__ Last year, [someone was tagged in Tremblant!](http://youtu.be/FCLdK09m5wo)\r\n\r\n**Best videolog:** The best participant video survival log gets you a __30$ Future Shop gift certificate.__\r\n\r\n**Survivor:** The first 10 Humans to arrive at the bar on Friday night win a popular __Zombie movie.__\r\n\r\n## Events\r\n**Rescue the Scientist:** Humans and Military must rescue the Scientist, held captive by Zombies. Each member of the winning side gets 5 bracelets.\r\n\r\n- *Location:* TBT Lawn\r\n- *Time:* Tuesday @ 6PM\r\n\r\n**Military Containment:** The Military protects socks by firing Nerf guns at Zombies. If Zombies or Humans get to the socks stash unharmed, they gain 10 bracelets.\r\n\r\n- *Location:* TBT lawn\r\n- *Time:* Wednesday @ 1PM\r\n\r\n**Amazing Race:** Starting from the University Centre, a horde of Zombies is chasing you around the city. Your survival depends on your ability to complete challenges to find 20 of bracelets to defend yourself.\r\n\r\n- *Location:* Announced the day of\r\n- *Time:* Thursday @ 11:30AM\r\n\r\n**Thrill the Mall:** Zombies invade the Rideau Centre and perform the Thriller dance. Participants gain 5 bracelets.\r\n\r\n- *Location:* UCU Agora\r\n- *Time:* Friday @ 5:30PM\r\n\r\n**Ultimate Challenge:** The final challenge awaits you at the after party. Come show off your skills and collect your prizes.\r\n\r\n- *Location:* Parliament Ultraclub\r\n- *Time:* Friday @ 8PM','## Missions GÃ©nÃ©rales\r\n**Dernier Humain en Vie:** Parvient Ã  survivre la semaine et gagner le DÃ©fi Ultime et tu gagnes un __PlayStation 3.__\r\n\r\n**Le plus de tags:** Tag le plus grand nombre d\'Humains et gagne un __XBOX 360.__\r\n\r\n**Meilleur tag filmÃ©:** Le meilleur vidÃ©o d\'un tag gagnera un __Ipod Touch.__\r\n\r\n**Le plus de bas:** Collectionne le plus grand nombre de bracelets Ã  bas HvsI et tu gagnes un __Ipod Nano.__\r\n\r\n**Cibles:** Plusieurs cÃ©lÃ©britÃ©s du campus, Ã  qui les noms seront dÃ©voilÃ©s pendant la semaine, seront ciblÃ©s. Tag une cÃ©lÃ©britÃ© et gagne un __certificat de 50$ Ã  EB Games.__\r\n\r\n**Photos:** Prenez-vous en photos [autour d\'Ottawa](/pdf/photo_list_f.pdf) avec votre t-shirt HvsI. La personne avec le plus de points gagnera un __certificat cadeau de 100$ au CafÃ© Nostalgica.__\r\n\r\n**Tag le plus Ã©loignÃ©:** Tag un Humain le plus loin du campus et vous gagnez les deux un __certificat cadeau de 50$ au 1848.__ [L\'an passÃ©, quelqu\'un s\'est fait taggÃ© Ã  Tremblant!](http://youtu.be/FCLdK09m5wo)\r\n\r\n**Meilleur log vidÃ©o:** Le meilleur vidÃ©o de l\'aventure de survie d\'un participant gagnera un __certificat cadeau de 30$ au Future Shop.__\r\n\r\n**Survivant:** Les premiers 10 Humains Ã  arriver au bar vendredi soir gagneront un __filme de zombie populaire.__\r\n\r\n## Ã‰vÃ©nements\r\n**Sauver le scientifique:** Les Humains et Militaires doivent secourir le scientifique, captif des Zombies. Chaque participant de l\'Ã©quipe gagnante gagne 5 bracelets.\r\n\r\n- *OÃ¹:* Terrasse TBT\r\n- *Quand?:* Mardi Ã  18h\r\n\r\n**Confinement militaire:** Les Militaires protÃ¨gent une pile de bas en tirant des Zombies avec des fusils Nerf. Si un Humain ou Zombie atteint les bas, il gagne 10 bracelets.\r\n\r\n- *OÃ¹:* Terrasse TBT\r\n- *Quand:* Mercredi Ã  13h\r\n\r\n**Course incroyable:** DÃ©butant au centre universitaire, tu dois te sauver des Zombies the chassant autour de la ville. Ta survie dÃ©pend de ta capacitÃ© d\'accomplir des Ã©preuves afin de trouver 20 bracelets pour te dÃ©fendre.\r\n\r\n- *OÃ¹:* AnnoncÃ© la journÃ©e mÃªme\r\n- *Quand?:* Jeudi Ã  11h30\r\n\r\n**Invasion du Centre Rideau:** Les Zombies envahissent le centre Rideau pour performer la dance de Thriller. Chaque participant gagne 5 bracelets.\r\n\r\n- *OÃ¹:* Agora UCU\r\n- *Quand?:* Vendredi Ã  17h30\r\n\r\n**DÃ©fi Ultime:** Le dÃ©fi ultime entre les derniers Humains prend place au party de clÃ´ture. DÃ©montrez vos talents et acceptez vos prix.\r\n\r\n- *OÃ¹:* Parliament Ultraclub\r\n- *Quand?:* Vendredi Ã  20h',0),
	(3,'2010-10-20 13:51:41','Party','Party','The closing ceremonies will be held at the [Parliament Ultraclub](http://www.facebook.com/event.php?eid=147647435280401) on November 5th and will start at 8PM.\r\n\r\nYou\'ll want to be there to see the last Humans compete in a series of challenges that will see only one lucky winner: The Last Human Alive!\r\n\r\nThis is also where we will be awarding prizes for the week\'s missions.\r\n\r\nStarting at 10PM is Masque-rave, THE headphone disco event of the year. Here\'s some info about that:\r\n\r\nGet ready for the event of the semester! The PIDSSA, the Faculty of Science, Economics, Psychology, Criminology and Humans VS Infected present the 2nd annual Masque-rave semi-formal on November 5th (Location: Parliament Ultraclub). Don\'t miss out on the chance to party with your friends across campus for a great cause as it is also the Movember kick off! This event will sell-out so buy your ticket at the PIDSSA or Crim office, or online at boutique.pidssa.ca starting October 19th for $5 in advance or $7 at the door. This will also be a Headphone Disco event, so remember to mark your calendars.\r\n\r\n19+ Event','La cÃ©rÃ©monie de clÃ´ture aura lieue au [Parliament Ultraclub](http://www.facebook.com/event.php?eid=147647435280401) le 5 novembre Ã  20h.\r\n\r\nVous allez voir les derniers Humains lutter l\'un contre l\'autre Ã©preuve aprÃ¨s Ã©preuve jusqu\'Ã  ce qu\'il n\'y ait qu\'un(e) gagnant(e): Le Dernier Humain en Vie!\r\n\r\nC\'est Ã  ce point que nous allons offrir les prix aux gagnants des missions.\r\n\r\nÃ€ partir de 22h, c\'est Masque-rave, l\'Ã©vÃ©nement Headphone Disco Ã  ne pas manquer. Voici plus de renseignements:\r\n\r\nÃŠtes-vous prÃªts et prÃªtes pour lâ€™Ã©vÃ©nement de la session? Lâ€™AÃ‰Ã‰PID, la FacultÃ© de sciences, Sciences Ã©conomiques, Psychologie, Criminologie et HVSI, vous prÃ©sentent le 2e Masque-rave le 5 novembre prochain. L\'Ã©vÃ¨nement se dÃ©roulera encore au Parliament Ultraclub. Ne manquez pas la chance de pouvoir faire la fÃªte avec vos amis dâ€™un cÃ´tÃ© Ã  lâ€™autre du campus. Câ€™est aussi la date du lancement de la campagne de Movember. Lâ€™Ã©vÃ¨nement se remplira rapidement, donc acheter vos billets aussi tÃ´t que possible au bureau de lâ€™AÃ‰Ã‰PID ou Crim, ou en ligne Ã  boutique.pidssa.ca dÃ¨s le 19 octobre. Le coÃ»t est de 5$ Ã  lâ€™avance et de 7$ Ã  la porte. Ce sera aussi un Ã©vÃ¨nement Â« Headphone Disco Â» qui vous permet de faire le choix des chansons Ã  lâ€™aide de vos Ã©couteurs! Alors, mettez-le Ã  votre agenda dÃ¨s maintenant.\r\n\r\nÃ‰vÃ¨nement 19+',0),
	(4,'2010-10-20 13:52:54','Rules','RÃ¨glements','**Every participant must read the rules before the game**\r\n\r\n**What\'s a tag?** A tag is a respectful touch by a Zombie\'s hand to a Human\'s body\r\n\r\n**Armband:** All participants must prominently display the appropriately coloured armband (provided) on their arm at all times during the game.\r\n\r\n**Safe Zones:** Zombies cannot tag Humans while they are in safe zones. The game is frozen for 30 seconds after a Human leaves a safe zone. The following areas are designated safe zones:\r\n\r\n- Bathrooms\r\n- Any Office (eg: Prof, Peer Help Center, Protection, dentist, etc.)\r\n- Classrooms\r\n- Quiet Study Rooms and Library\r\n- SITE + UCU Cafeterias (where you buy food, not the eating area)\r\n- Tape-delimited areas around check-in tables (CBY, UCU, CafÃ© Alt)\r\n- 1848\r\n\r\n**Boundaries:** The game has no geographical boundaries. Extra points for a tag in another country!\r\n\r\n### Human Rules\r\n\r\n**Game Card:** Humans must keep their game card (provided) on them at all times.\r\n\r\n**Check Ins:** Humans must physically check in at a check-in location twice a day, between 8:30 and 5:30, with at least 4 hours between check-ins. Failure to do this will result in becoming a Zombie.  [Participants can check-in online once during the week.](/webcheckin)\r\n\r\n**Check-in Locations:** CBY basement, SFUO office, CafÃ© Alt from 8:30AM to 5:30PM\r\n\r\n**Tagged By a Zombie:** When tagged by a Zombie, a Human is required to give the Zombie their game card. You automatically become a Zombie when the Zombie reports the tag, but you can only start tagging once you\'ve exchanged your white armband for a green one at a check-in location (SFUO office excluded).\r\n\r\n**Stunning a Zombie:** You can throw/wield an official HvsI sock (your own CLEAN sock wrapped in a provided bracelet) at a Zombie to freeze them for 2 minutes. The Zombie keeps the sock.\r\n\r\n### Zombie Rules\r\n\r\n**Tagging:** When a Zombie tags a Human, the Zombie must take their victim\'s game card and report the tag asap using one of the following methods:\r\n\r\n- Email tag@HvsI.ca with the victim\'s game ID as the subject and using the email address used in registration\r\n- Tweet the victim\'s game ID with the #HvsI hashtag (using the twitter account in your profile)\r\n- In person at a check-in location\r\n- Online at www.HvsI.ca by entering the victim\'s game ID in the \"Register a Tag\" box in the sidebar\r\n\r\n**Getting Stunned:** When hit with an official sock by a Human (Or a Nerf gun dart from Military), a Zombie is stunned for 2 minutes. A stunned zombie can move but may not interact with the game in any way. This includes shielding other zombies from socks or following a human. The Zombie keeps the sock.','**Chaque participant doit lire les reglements avant de jouer**\r\n\r\n**Qu\'est-ce qu\'un tag?** Un tag est quand la main d\'un Zombie touche le corps d\'un Humain de faÃ§on respectueuse.\r\n\r\n**Brassard:** Tous les participants doivent porter le brassard de la couleur appropriÃ©e (fourni) sur leurs bras en tout temps.\r\n\r\n**Zones sÃ©cures:** Un Zombie ne peut pas tagger un Humain dans une zone sÃ©cure. L\'Humain est sÃ©cure pour 30 secondes aprÃ¨s qu\'il ait quittÃ© une zone sÃ©cure. Les endroits suivants sont considÃ©rÃ©es des zones sÃ©cures:\r\n\r\n- Salles de bain\r\n- Tout bureau (ex: prof, centre d\'aide, protection, dentiste, etc.)\r\n- Salles de classe\r\n- Salles d\'Ã©tude tranquilles et bibliothÃ¨que\r\n- CafÃ©tÃ©rias de SITE et UCU (oÃ¹ ils vendent la bouffe, pas lÃ  oÃ¹ tu manges)\r\n- Zones dÃ©limitÃ©es autour des tables d\'enregistrement (CBY, FÃ‰UO, CafÃ© Alt)\r\n- 1848\r\n\r\n**Limites:** Le jeu n\'a aucune limite gÃ©ographique. Points d\'extra pour un tag dans un autre pays!\r\n\r\n### RÃ¨glements Humains\r\n\r\n**Carte de jeu:** Un Humain doit garder sa carte de jeu (fournie) sur soi en tout temps.\r\n\r\n**Renouvellement:** Un Humain doit se prÃ©senter Ã  une table d\'enregistrement 2 fois par jour, entre 8h30 et 17h30, avec au moins 4 heures d\'intervalle. Faire autrement transformera l\'Humain en Zombie. [Un seul renouvellement en ligne est permis.](/webcheckin)\r\n\r\n**Tables d\'enregistrement:** Sous-sol CBY, bureau FÃ‰UO, CafÃ© Alt de 9h Ã  17h.\r\n\r\n**TaggÃ© par un Zombie:** Une fois taguÃ© par un Zombie, un Humain doit lui donner sa carte de jeu. L\'Humain devient automatiquement Zombie mais peut seulement tagger une fois son brassard blanc Ã©changÃ© pour un vert Ã  une table d\'enregistrement (sauf FÃ‰UO).\r\n\r\n**Geler un Zombie:** Un Humain peut geler un Zombie pour 2 minutes en lui lanÃ§ant un bas HvsI (un bas PROPRE que vous avez entourÃ© avec un bracelet fourni). Le Zombie garde le bas.\r\n\r\n### RÃ¨glements Zombie\r\n\r\n**Tagger:** Quand un Zombie tag un Humain, le Zombie doit prendre la carte de jeu de la victime et reporter le tag aussitÃ´t que possible en utilisant l\'une des mÃ©thodes suivantes:\r\n-Envoyer un courriel Ã  tag@HvsI.ca avec l\'ID de jeu de la victime avec le courriel utilisÃ© pour s\'enregistrer au jeu.\r\n\r\n- Tweeter l\'ID de jeu de la victime avec le hashtag #HvsI\r\n- Reporter le tag en personne Ã  une table d\'enregistrement\r\n- En ligne Ã  www.HvsI.ca en entrant l\'ID de jeu de la victime dans la boÃ®te \"Enregistrer un tag\"\r\n\r\n**Se faire gelÃ©:** Un Zombie frappÃ© par un bas officiel (ou un dart Nerf tirÃ© par un Militaire) est gelÃ© pour 2 minutes. Un Zombie gelÃ© peut bouger mais ne peut pas intÃ©ragir avec le jeu d\'aucune faÃ§on. Ceci comprends continuer de courir vers un Humain. Le Zombie garde le bas.',0),
	(5,'2010-10-20 13:53:55','Station Operations','Who Cares?','**Players must wear armbands at <span style=\"font-size: 1.4em\">all</span> times**\r\n\r\n1. There are 2 \"table kits\" containing: a laptop, sock bracelets,\r\n   t-shirts, armbands, blank business cards and a cashbox + sales sheet.\r\n2. One kit will be in the ESS office and the other in the SFUO office\r\n   (ask Ted or Alex).\r\n3. The first person takes the kit @8:30, last person brings it back\r\n   @5:30.\r\n4. The laptops will be permanently signed in, so don\'t sign out!\r\n5. When someone gets their kit, you must create an account for them or\r\n   verify that their student number is correct if they\'ve already registered\r\n   online. If they\'ve already registered, you need to confirm that they\r\n   received their kit by entering their student number at player activation (in station operations).\r\n6. Creating an account: Go to hvsi.ca/register and force the Human to\r\n   fill in the details.\r\n7. What\'s in a kit?:\r\n      1. Game card (you need to write down their game ID)\r\n      2. White armband\r\n      3. Bracelets: 6 Monday before 1PM, 4 Monday after 1PM, 2 Tuesday\r\n      4. T-shirt (optional: costs 5$)\r\n8. When you make a sale, update the sheet in the cashbox.\r\n9. Always try to arrive a bit early, the person before you might have to\r\n   leave for class. If you can\'t make a shift, get someone to do it for you.\r\n10. If the person after you is late and you have to leave, temporarily\r\n   return the kit to the ESS/SFUO/Arts office.\r\n11. Tell people to read the rules and that the bracelets can only freeze\r\n   Zombies when wrapped around a sock.','Who really fucking cares?',0);

/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table score
# ------------------------------------------------------------



# Dump of table snapshot
# ------------------------------------------------------------



# Dump of table station
# ------------------------------------------------------------

LOCK TABLES `station` WRITE;
/*!40000 ALTER TABLE `station` DISABLE KEYS */;

INSERT INTO `station` (`id`, `location`, `child_name`)
VALUES
	(2,'cby',NULL),
	(3,'ucu',NULL),
	(4,'cafealt',NULL),
	(5,'twitter',NULL),
	(6,'email',NULL),
	(7,'internet',NULL);

/*!40000 ALTER TABLE `station` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table tag
# ------------------------------------------------------------



# Dump of table twitter
# ------------------------------------------------------------



# Dump of table user
# ------------------------------------------------------------

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;

INSERT INTO `user` (`id`, `name`, `username`, `hashed_pass`, `language`, `student_num`, `email`, `twitter`, `cell`, `creation_time`, `child_name`)
VALUES
	(1,'admin','admin','$2a$12$syvVzCn2PZETYgZ/24Mc1OagnhmVibt5muTHX2krrBAud/YVPuL0y','e',0,'admin@hvsi.ca',NULL,NULL,NULL,'Admin'),
	(2,'cby','cby','$2a$12$FdG.nMPsPFIRQZcyuWPEF.SlAyoLaBUs0IgjrGBi6oiNjWPBNf8MG','e',1,'cby@hvsi.ca',NULL,NULL,NULL,'Station'),
	(3,'ucu','ucu','$2a$12$BrJf0YdhdttCWuBFmwzq7eTFYuSzXeWRnrZETRHXDXg4cA6sQJh8O','e',2,'ucu@hvsi.ca',NULL,NULL,NULL,'Station'),
	(4,'cafealt','cafealt','$2a$12$E64PTd3N7UD8G8fPY1qdQOT3HC9lP8UaikV0/V5TLWddZByrHGHbe','e',3,'cafealt@hvsi.ca',NULL,NULL,NULL,'Station'),
	(5,'zombie_twitter','zombie_twitter','$2a$12$6rd51hELNco633cRot7gi.sJwqkgbm536oDxAr/cl7gmvEv96Q4h2','e',4,'twitter@hvsi.ca',NULL,NULL,NULL,'Station'),
	(6,'zombie_email','zombie_email','$2a$12$w11K.NVR9zJ6Kloss1fShuymT4i/bD.ta4JgWaG0tyoEvlwxjEA4i','e',5,'email@hvsi.ca',NULL,NULL,NULL,'Station');

/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
