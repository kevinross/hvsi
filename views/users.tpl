%if 'i18n' not in globals():
	%from i18n import i18n
%end
%import calendar
%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<table border="1" style="width: 100%;">
					<tr>
						%i=i18n[lang]['pages'][page]['table']
						<td><strong>{{i['id']}}</strong></td>
						<td><strong>{{i['username']}}</strong></td>
						<td><strong>{{i['game_id']}}</strong></td>
						<td><strong>{{i['name']}}</strong></td>
						<td><strong>{{i['status']}}</strong></td>
						<td><strong>{{i['signedin']}}</strong></td>
						%del i
					</tr>
%				  for player in users:
					<tr>
						<td><strong>{{player.id}}</strong></td>
						<td><a href="/user/{{player.username}}">{{player.username}}</a></td>
						<td>{{player.game_id}}</td>
						<td>{{player.name}}</td>
						<td>{{i18n[lang]['player_status'][player.state]}}</td>
						<td>{{i18n[lang]['pages']['register']['yes'] if player.signedin else i18n[lang]['pages']['register']['no']}}</td>
					</tr>
%				  end
				</table>
				<br/>
				<br/>
			</div>
%cinclude parts part=3
</body>
</html>