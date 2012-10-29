%if 'i18n' not in globals():
	%from i18n import i18n
%end
%import calendar
%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<h3>{{i18n[lang]['pages'][page]['search_heading']}}</h3>
				<form method="POST" action="/users">
				{{i18n[lang]['pages'][page]['match_on']}} 
					<select name="cat">
						<option value="email">{{i18n[lang]['pages']['register']['email']}}</option>
						<option value="twitter">{{i18n[lang]['pages']['register']['twitter']}}</option>
						<option value="cell">{{i18n[lang]['pages']['register']['cell']}}</option>
						<option value="student">{{i18n[lang]['pages']['register']['student_num']}}</option>
						<option value="game_id">Game ID</option>
					</select>
					&nbsp;
					<input type="textbox" name="value" />
					<input type="submit" value="{{i18n[lang]['pages'][page]['retrieve']}}" />
				</form>
				<br/>
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