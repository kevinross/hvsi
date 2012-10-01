%if 'i18n' not in globals():
	%from i18n import i18n
%end
%import calendar, random, string
%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<h2>{{i18n[lang]['pages'][page]['title']}}</h2>
				<form action="/tag" method="post">
					<div>
						<label for="taggee">
							{{i18n[lang]['player_status']['human']}} {{i18n[lang]['pages']['register']['gameid']}}:
						</label>
					</div>
					<div>
						<input type="textbox" name="taggee"/>
					</div>
					<input type="hidden" name="uid" value="webform_{{''.join(random.sample(string.ascii_letters+string.digits, 36))}}" />
					<div>
						<label for="submit">
							&nbsp;
						</label>
					</div>
					<div>
						<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['tag']}}" />
					</div>
				</form>
			</div>
%cinclude parts part=3
</body>
</html>