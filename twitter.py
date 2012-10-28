import urllib, re
from lxml import etree

class tweet:
	url_regex = re.compila(r"(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))")
	def __init__(self, username=None,
					   list_=None,
					   favorites=False,
					   query=None,
					   avatar_size=None,
					   count=3,
					   fetch=None,
					   page=1,
					   retweets=True,
					   intro_text=None,
					   outro_text=None,
					   join_text=None,
					   auto_join_text_default=" I said, ",
					   auto_join_text_ed= " I ",
					   auto_join_text_ing= " I am ",
					   auto_join_text_reply= " I replied to ",
					   auto_join_text_url= " I was looking at ",
					   loading_text=None,
					   refresh_interval=None,
					   twitter_url='twitter.com',
					   twitter_api_url='api.twitter.com',
					   twitter_search_url='search.twitter.com',
					   template='{avatar}{time}{join} {text}',
					   comparator=lambda t1,t2:(t2['tweet_time'] - t1['tweet_time']),
					   filter_=lambda x: True):
		self.__dict__.update(locals().copy())
		del self.__dict__['self']
	
	def t(self, template, info):
		if isinstance(template, basestring):
			result = template
			for key in info:
				val = info[key] or ''
				result = val.join(result.split('{'+key+'}'))
			return result
		else return template(info)
	
	def replacer(self, regex, replacement):
		def func(strings):
			returning = []
			for s in strings:
				returning.append(re.sub(regex, replacement, s))
			return returning
		return func