%cinclude part_html_decl
<head>
%	cinclude head
</head>
%cinclude part_html_body
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
%cinclude part_html_sidebar
</body>
</html>
