			<ul id="navigation">
%import database as db
%rego = db.Game.is_reg
%logged_in = (hasattr(request, 'logged_in') and request.logged_in)
%player = (logged_in and request.player)
%station = (logged_in and request.station)
%superuser = (logged_in and (request.admin or request.station))
%for_player = 2
%for_station = 3
%for_all  = 4
%reg_open  = 5
				<li class="page_item {{"current_page_item" if request.path=='/' else ""}}"><a href="/" title="{{i18n[lang]['nav'][0][1]}}">{{i18n[lang]['nav'][0][1]}}</a></li>
%			for i in i18n[lang]['nav'][1:]:
%			  if (logged_in and player and i[for_player] and i[for_all]) or \
%				 (not logged_in and i[for_all]) or \
%				 (logged_in and superuser and i[for_station]):
%				if not rego and i[0] == 'register':
%					continue
%				end
				<li class="page_item {{"current_page_item" if i[0] in request.path else ""}}"><a href="/{{i[0]}}" title="{{i[1]}}">{{i[1]}}</a></li>
%			  end
%			end
%			  if hasattr(request, 'logged_in') and request.logged_in and not request.station:
				<li class="page_item {{"current_page_item" if ('/user/' + request.user.username) in request.path else ""}}"><a href="/user/{{request.user.username}}">{{i18n[lang]['profile']}}</a></li>
%			  end
%			  if hasattr(request, 'admin') and request.admin:
				<li class="page_item {{"current_page_item" if 'game' in request.path else ""}}"><a href="/game" title="{{i18n[lang]['navd']['game']}}">{{i18n[lang]['navd']['game']}}</a></li>
%			  end
				<li class="page_item" style="float:right;"><a href="?lang={{i18n[lang]['altlang']['key']}}">{{i18n[lang]['altlang']['name']}}</a></li>
			</ul>
