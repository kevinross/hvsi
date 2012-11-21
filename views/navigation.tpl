			<ul id="navigation">
%rego = db.Game.is_reg
%starto = db.Game.is_started
%logged_in = (hasattr(request, 'logged_in') and request.logged_in)
%player = (logged_in and request.player)
%station = (logged_in and request.station)
%superuser = (logged_in and (request.admin or request.station))
%def build_list(key):
				<li class="page_item {{"current_page_item" if key in request.path else ""}}"><a href="/{{key}}" title="{{i18n[lang]['nav'][key]}}">{{i18n[lang]['nav'][key]}}</a></li>
%end
				<li class="page_item {{"current_page_item" if request.path=='/index' else ""}}"><a href="/index" title="{{i18n[lang]['nav']['home']}}">{{i18n[lang]['nav']['home']}}</a></li>
%for i in ('blog', 'missions', 'party'):
%	build_list(i)
%end
%if rego or station or superuser:
%	build_list('register')
%end
%build_list('rules')
%if starto or superuser:
%	build_list('stats')
%end
%if station or superuser:
%	build_list('station')
%end
%			  if hasattr(request, 'logged_in') and request.logged_in and not request.station:
				<li class="page_item {{"current_page_item" if ('/user/' + request.user.username) in request.path else ""}}"><a href="/user/{{request.user.username}}">{{i18n[lang]['profile']}}</a></li>
%			  end
%			  if hasattr(request, 'admin') and request.admin:
				<li class="page_item {{"current_page_item" if 'game' in request.path else ""}}"><a href="/game" title="{{i18n[lang]['navd']['game']}}">{{i18n[lang]['navd']['game']}}</a></li>
%			  end
				<li class="page_item" style="float:right;"><a href="?lang={{i18n[lang]['altlang']['key']}}">{{i18n[lang]['altlang']['name']}}</a></li>
			</ul>
