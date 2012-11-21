%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<h2>{{i18n[lang]['pages'][page]['title']}}</h2>
%			  if request.user.did_webcheckin:
				<h4>{{i18n[lang]['pages'][page]['already']}}</h4>
%			  else:
				<h4>{{i18n[lang]['pages'][page]['notice']}}</h4>
				<form action="/webcheckin" method="post">
					<div>
						<label for="confirm">{{i18n[lang]['pages'][page]['confirm']}}:</label>
					</div>
					<div>
						<input type="checkbox" name="confirm" />
					</div>
					<div>
						<label for="submit">&nbsp;</label>
					</div>
					<div>
						<input type="submit" value="{{i18n[lang]['pages'][page]['title']}}" />
					</div>
				</form>
%			  end
				<br/>
				<br/>
				<br/>
			</div>
%cinclude parts part=3
</body>
</html>
