%import random, string
%cinclude part_html_decl
<head>
%	cinclude head
</head>
%cinclude part_html_body
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
%cinclude part_html_sidebar
</body>
</html>
