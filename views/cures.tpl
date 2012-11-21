%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<form action="/cures/add" method="post">
					<input type="submit" value="{{i18n[lang]['pages'][page]['addcure']}}" style="float:left;"/>
				</form>
				<form action="/cures/massdelete" method="post">
					<input type="submit" value="{{i18n[lang]['pages'][page]['deletecures']}}" />
					<table border="1" style="width: 100%;">
						<tr>
							%i=i18n[lang]['pages'][page]['table']
							<td><strong>{{i['id']}}</strong></td>
							<td><strong>{{i['cardid']}}</strong></td>
							<td><strong>{{i['expiry']}}</strong></td>
							<td><strong>{{i['used']}}</strong></td>
							<td><strong>{{i['time']}}</strong></td>
							<td><strong>{{i['username']}}</strong></td>
							<td><strong>{{i['disqualified']}}</strong></td>
							<td><strong>{{i['delete']}}</strong></td>
							%del i
						</tr>
%					  for cure in cures:
						<tr>
							<td><strong>{{cure.id}}</strong></td>
							<td>{{cure.card_id}}</td>
							<td>{{'' if not cure.expiry else cure.expiry.isoformat()}}</td>
							<td>{{i18n[lang]['pages']['register']['yes'] if cure.used else i18n[lang]['pages']['register']['no']}}</td>
							<td>{{'' if not cure.used else cure.time.isoformat()}}</td>
							<td><a href={{'""' if not cure.used else ('"/user/' + cure.player.username + '"')}}>{{'' if not cure.used else cure.player.username}}</a></td>
							<td>{{i18n[lang]['pages']['register']['yes'] if cure.disqualified else i18n[lang]['pages']['register']['no']}}</td>
							<td><input type="checkbox" name="cure_{{cure.id}}" /></td>
							<td><a href="/cures/edit/{{cure.id}}">Edit</a></td>
						</tr>
%					  end
					</table>
					<br/>
					<br/>
			</div>
%cinclude parts part=3
</body>
</html>
