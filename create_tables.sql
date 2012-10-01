CREATE TABLE `admin` (
  `id` int(11) NOT NULL auto_increment,
  `child_name` varchar(255) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
CREATE TABLE `checkin` (
  `id` int(11) NOT NULL auto_increment,
  `time` datetime NOT NULL,
  `location` enum('cby','ucu','cafealt','manual') NOT NULL,
  `player_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `checkin_player_id_exists` (`player_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL auto_increment,
  `time` datetime NOT NULL,
  `content` text,
  `user_id` int(11) default NULL,
  `post_id` int(11) default NULL,
  PRIMARY KEY  (`id`),
  KEY `comment_user_id_exists` (`user_id`),
  KEY `comment_post_id_exists` (`post_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
CREATE TABLE `cure` (
  `id` int(11) NOT NULL auto_increment,
  `time` datetime NOT NULL,
  `card_id` varchar(10) NOT NULL,
  `used` tinyint(1) NOT NULL,
  `disqualified` tinyint(1) NOT NULL,
  `player_id` int(11),
  PRIMARY KEY  (`id`),
  UNIQUE KEY `card_id` (`card_id`),
  KEY `cure_player_id_exists` (`player_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
CREATE TABLE `player` (
  `id` int(11) NOT NULL auto_increment,
  `state` enum('human','zombie','inactive','banned') NOT NULL,
  `game_id` varchar(10) default NULL,
  `signedin` tinyint(1) NOT NULL,
  `signedin_time` datetime default NULL,
  `child_name` varchar(255) default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `game_id` (`game_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
CREATE TABLE `post` (
  `id` int(11) NOT NULL auto_increment,
  `time` datetime NOT NULL,
  `title_e` text,
  `title_f` text,
  `content_e` text,
  `content_f` text,
  `allow_comments` tinyint(1) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
CREATE TABLE `station` (
  `id` int(11) NOT NULL auto_increment,
  `location` enum('cby','ucu','cafealt','manual') NOT NULL,
  `child_name` varchar(255) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL auto_increment,
  `time` datetime NOT NULL,
  `tagger_id` int(11) NOT NULL,
  `taggee_id` int(11) NOT NULL,
  `uid` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `uid` (`uid`),
  KEY `tag_tagger_id_exists` (`tagger_id`),
  KEY `tag_taggee_id_exists` (`taggee_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
CREATE TABLE `twitter` (
  `id` int(11) NOT NULL auto_increment,
  `text` text,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
CREATE TABLE `user` (
  `id` int(11) NOT NULL auto_increment,
  `name` text NOT NULL,
  `username` varchar(25) NOT NULL,
  `hashed_pass` text NOT NULL,
  `language` enum('e','f') NOT NULL,
  `student_num` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `twitter` varchar(50) default NULL,
  `cell` varchar(11) default NULL,
  `creation_time` datetime default NULL,
  `child_name` varchar(255) default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `student_num` (`student_num`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `twitter` (`twitter`),
  UNIQUE KEY `cell` (`cell`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;