%if 'i18n' not in globals():
	%from i18n import i18n
%end
%import calendar
%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<h1>{{i18n[lang]['pages'][page]['title']}}</h1>
				<form action="/login" method="post">
					<div class="form_label">
					  <label for="username">
						{{i18n[lang]['pages']['register']['username']}}:
					  </label>
					</div>
					<div class="form_field">
						<input type="textbox" name="username" />
					</div>
					<div class="form_label">
					  <label for="password">
						{{i18n[lang]['pages']['register']['password']}}:
					  </label>
					</div>
					<div class="form_field">
						<input type="password" name="password" />
					</div>
					<div class="form_label">
					  <label for="submit">
					  	&nbsp;
					  </label>
					</div>
					<div class="form_field">
						<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['title']}}" />
					</div>
				</form>
				<br/>
				<br/>
				<br/>
			</div>
%cinclude parts part=3
</body>
</html>