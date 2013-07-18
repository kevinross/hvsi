%admin = bottle.request.admin or bottle.request.station
%path = re.match(r'/log[inout]*(.*)', bottle.request.path)
%count = db.Game.is_countdown
%if (not admin and count and not path):
%bottle.redirect('/', 302)
%end
<body id="mainBody">
	<div id="pagewidth" class="clearfix">
		<div id="header">
			<div class="logo">
				<a href="/"></a>
			</div>
%if 'nologin' not in globals() or ('nologin' in globals() and not nologin):
  %if 'login' not in request.path:
		  <div id="loginheader" style="float: right;">
%		cinclude login_header
		  </div>
  %end
%end
%		cinclude navigation
		</div>
%if not ('nocontent' in globals() and nocontent):
		<div id="content">
			<div id="left">
              %if get('title', i18n[lang]['pages'][page]['title']):
                <h1>{{get('title', i18n[lang]['pages'][page]['title'])}}</h1>
              %end
%			  if bottle.request.session.error:
				<div style="color: red;">
%if get('suberror', None):
					{{i18n[lang]['pages'][page][bottle.request.session.error] % i18n[lang]['pages'][page][suberror]}}
%else:
					{{i18n[lang]['pages'][page][bottle.request.session.error]}}
%end
				</div>
				<br/>
%				bottle.request.session.error = None
%			  end