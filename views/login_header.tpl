%from hvsi.imports import *
%		if not request.logged_in:
%		  if 'login' not in request.path:
			<div class="fr" style="float: right;">
				<form action="/login" method="post">
					{{i18n[lang]['pages']['register']['username']}}: <input type="text" name="username" /> 
					{{i18n[lang]['pages']['register']['password']}}: <input type="password" name="password" /> 
					<input type="submit" class="header_login_submit" value="{{i18n[lang]['pages']['login']['title']}}"/>
				</form>
			</div>
%		  end
%		else:
			<div class="fr" style="float: right;">
%			  if not request.station:
				<a href="/user/{{request.user.username}}">
%			  end
				{{request.user.name}} ({{request.user.username}})
%			  if not request.station:
				</a>
				<span style="margin-left: 5px; margin-right: 5px">|</span>
				<a href="/logout">{{i18n[lang]['logout']}}</a>
%			  end
			</div>
%		end
