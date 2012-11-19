%from hvsi.imports import *
%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<h2>
					<a href="/user/{{tagger.username}}">{{tagger.username}}</a>
%				  if 'taggee' in globals():
					&nbsp;{{i18n[lang]['pages'][page]['vs']}}&nbsp;
					<a href="/user/{{taggee.username}}">{{taggee.username}}</a>
%				  end
				</h2>
				<form action="/tagrm" method="post">
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['submit']}}" />
					<table border="1" style="width: 100%;">
						<tr>
							%i=i18n[lang]['pages'][page]['table']
							<td><strong>{{i['id']}}</strong></td>
							<td><strong>{{i['method']}}</strong></td>
							<td><strong>{{i['time']}}</strong></td>
							<td><strong>{{i['killer']}}</strong></td>
							<td><strong>{{i['victim']}}</strong></td>
							<td><strong>{{i['delete']}}</strong></td>
							<td><strong>{{i['cure']}}</strong></td>
							%del i
						</tr>
%					  for tag in tags:
						<tr>
							<td><strong>{{tag.id}}</strong></td>
							<td>{{tag.method}}</td>
							<td>{{tag.time.isoformat()}}</td>
							<td><a href="/user/{{tag.tagger.username}}">{{tag.tagger.username}}</a></td>
							<td><a href="/user/{{tag.taggee.username}}">{{tag.taggee.username}}</a></td>
							<td><input type="checkbox" name="{{'rm' + tag.time.isoformat()+'/'+tag.tagger.username+'/'+tag.taggee.username}}" />
							<td><input type="checkbox" name="{{'cu' + tag.time.isoformat()+'/'+tag.tagger.username+'/'+tag.taggee.username}}" />
						</tr>
%					  end
					</table>
					<br/>
					<br/>
				</form>
			</div>
%cinclude parts part=3
</body>
</html>