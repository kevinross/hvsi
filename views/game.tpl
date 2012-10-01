%if 'i18n' not in globals():
	%from i18n import i18n
%end
%import calendar, database as db
%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<h2>{{i18n[lang]['pages'][page]['title']}}</h2>
				<form action="/game" method="post">
%				  if db.Game.is_started:
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['end']}}" />
%				  else:
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['start']}}" />
%				  end
				</form>
				<br/>
				<form action="/reg" method="post">
%				  if db.Game.is_reg:
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['endr']}}" />
%				  else:
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['startr']}}" />
%				  end
				</form>
				<br/>
				<a href="/email">Send Email</a>
				<br/>
			</div>
%cinclude parts part=3
</body>
</html>