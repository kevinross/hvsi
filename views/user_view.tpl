%if 'i18n' not in globals():
	%from i18n import i18n
%end
%import calendar, markdown, database as db
%cinclude parts part=1
<head>
%	cinclude head
	<style>
		.u_key {
			float: left;
			font-weight: bold;
		}
		.u_value {
			float: right;
		}
	</style>
</head>
%cinclude parts part=2
				<div style="width: 50%;">
					<h2>{{vuser.username}}<span style="font-size: 0.5em; float: right;"><a href="/user/{{vuser.username}}/edit">[{{i18n[lang]['pages'][page]['edit']}}]</a></span></h2>
				  %i=i18n[lang]['pages']['register']
%				  for j in ['username','name','email','student_num','twitter','cell']:
%					v = getattr(vuser, j)
%					if v == 0:
%						v = '0'
%					end
					<span class="u_key">{{i[j]}}:</span>&nbsp;<span class="u_value">{{v if v else ('[' + i18n[lang]['pages'][page]['none'] + ']')}}</span><br/>
%				  end
%				  if hasattr(vuser, 'game_id') and (vuser.is_human() or request.admin):
					<span class="u_key">{{i['gameid']}}:</span> <span class="u_value">{{vuser.game_id}}</span><br/>
					<span class="u_key">{{i18n[lang]['player_status']['active']}}:</span> <span class="u_value">{{i['yes'] if vuser.signedin else i['no']}}</span><br/>
%				  end
				  %del i
				</div>
%			  if (hasattr(vuser, 'signedin') and not vuser.signedin) and (request.station or request.admin) and db.Game.is_reg:
				<br/>
				<h3>{{i18n[lang]['pages'][page]['activate']}}</h3>
				<form action="/user/{{vuser.username}}/activate" method="post">
					<span>
						<input type="checkbox" name="kitted" />
						<label for="kitted">{{i18n[lang]['pages'][page]['kitted']}}</label>
					</span>
					<div>
						<label for="submit">
							&nbsp;
						</label>
					</div>
					<div>
						<input type="submit" value="{{i18n[lang]['pages'][page]['activate']}}" />
					</div>
				</form>
				<br/>
%			  end
%			  if hasattr(vuser, 'game_id'):
				<br/><br/>
				<div style="width: 50%;">
				%i=i18n[lang]['pages'][page]
					<h3>{{i['stats']}}</h3>
					<span class="u_key">{{i18n[lang]['player_status']['state']}}:</span> <span class="u_value">{{i18n[lang]['player_status'][vuser.state]}}</span><br/>
					<span class="u_key">{{i['kills']}}:</span> <span class="u_value">{{vuser.kills.count()}}</span><br/>
					<span class="u_key">{{i['deaths']}}:</span> <span class="u_value">{{vuser.deaths.count()}}</span><br/>
					<span class="u_key">{{i['cures']}}:</span> <span class="u_value">{{vuser.cures.count()}}</span><br/>
				%c = vuser.last_checkin
					<span class="u_key">{{i['checkin']}}:</span> <span class="u_value">{{'' if not c else (c.time.strftime("%H:%M") + ' @ ' + c.location.upper())}}</span></br/>
				%del c
				</div>
				<br/>
%			  if hasattr(request, 'admin') and request.admin:
				<div style="width: 58%;">
					<span class="u_key"><a href="/tag/{{vuser.username}}">{{i18n[lang]['pages'][page]['tags']}}</a></span>
					<form action="/user/{{vuser.username}}/tags" method="post">
						&nbsp;{{i18n[lang]['pages'][page]['and']}}
						<span class="u_value"><input type="textbox" name="username" />
						<input type="submit" name="submit" value="submit" style="display:none;" />
					</form>
				</div>
				<br/>
				<span class="u_key"><a href="/user/{{vuser.username}}/checkins">{{i18n[lang]['pages'][page]['checkins']}}</a></span>
%			  end
%			  end
				<br/>
			</div>
%cinclude parts part=3
</body>
</html>
