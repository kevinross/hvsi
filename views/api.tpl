%if method=='kills':
{
	'result': [
%			for kill in kills:
				{'tagger': kill.tagger.username,
				 'taggee': kill.taggee.username,
				 'time':   kill.time.isoformat()
				}
%			end
			]
}