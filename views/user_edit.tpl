%if 'i18n' not in globals():
	%from i18n import i18n
%end
%import calendar
%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<h2>{{vuser.username}}</h2>
				<form action="/user/{{vuser.username}}/edit" method="post">
%				  if request.admin:
					<h3>{{i18n[lang]['pages'][page]['userinfo']}}</h3>
					<div>
						<label for="username">
							{{i18n[lang]['pages']['register']['username']}}:
						</label>
					</div>
					<div>
						<input type="textbox" name="username" value="{{vuser.username}}" />
					</div>
					<div>
						<label for="name">
							{{i18n[lang]['pages']['register']['name']}}:
						</label>
					</div>
					<div>
						<input type="textbox" name="name" value="{{vuser.name}}" />
					</div>
					<div>
						<label for="student_num">
							{{i18n[lang]['pages']['register']['student_num']}}:
						</label>
					</div>
					<div>
						<input type="textbox" name="student_num" value="{{vuser.student_num}}" />
					</div>
%				   if hasattr(vuser, 'state'):
					<div>
						<label for="state">
							{{i18n[lang]['player_status']['state']}}:
						</label>
					</div>
					<div>
						<select name="state">
						  %for k in [x for x in i18n[lang]['player_status'].keys() if x != 'state' and x != 'active']:
							<option value="{{k}}" {{'selected="1"' if vuser.state == k else ''}}>{{i18n[lang]['player_status'][k]}}</option>
						  %end
						</select>
					</div>
%				   end
%				  end
					<div>
						<label for="email">
							{{i18n[lang]['pages']['register']['email']}}:
						</label>
					</div>
					<div>
						<input type="textbox" name="email" value="{{vuser.email}}" />
					</div>
					<div>
						<label for="cell">
							{{i18n[lang]['pages']['register']['cell']}}:
						</label>
					</div>
					<div>
						<input type="textbox" name="cell" value="{{vuser.cell if vuser.cell else ''}}" />
					</div>
					<div>
						<label for="twitter">
							{{i18n[lang]['pages']['register']['twitter']}}:
						</label>
					</div>
					<div>
						<input type="textbox" name="twitter" value="{{vuser.twitter if vuser.twitter else ''}}" />
					</div>
					<br/>
					<h3>{{i18n[lang]['pages']['register']['language']}}</h3>
					<div>
						<select name="language">
							<option value="e" {{'selected="1"' if vuser.language=='e' else ''}}>English</option>
							<option value="f" {{'selected="1"' if vuser.language=='f' else ''}}>Français</option>
						</select>
					</div>
					<br/>
					<h3>{{i18n[lang]['pages'][page]['passchange']}}</h3>
%				  if not request.admin:
					<div>
						<label for="verify_password">
							{{i18n[lang]['pages'][page]['oldpass']}}:
						</label>
					</div>
					<div>
						<input type="password" name="verify_password" />
					</div>
%				  end
					<div>
						<label for="password">
							{{i18n[lang]['pages']['register']['password']}}:
						</label>
					</div>
					<div>
						<input type="password" name="password" />
					</div>
					<div>
						<label for="confirm_password">
							{{i18n[lang]['pages']['register']['password_confirm']}}:
						</label>
					</div>
					<div>
						<input type="password" name="confirm_password" />
					</div>
					<div>
						<label for="submit">
							&nbsp;
						</label>
					</div>
					<div>
						<input type="submit" value="{{i18n[lang]['pages']['user']['edit']}}" />
					</div>
				</form>
				<br/>
			  %if hasattr(vuser, 'zero') and not vuser.zero and request.admin:
				<h3>{{i18n[lang]['pages'][page]['zero']}}</h3>
				<form action="/user/{{vuser.username}}/zero" method="post">
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['makezero']}}" />
				</form>
				<br/>
			  %end
			</div>
%cinclude parts part=3
</body>
</html>