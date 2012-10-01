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
%			  if 'success' in request.params:
					<div><strong>{{i18n[lang]['pages'][page]['success']}}</strong></div>
%			  else:
				<form action="/password_reset" method="post">
					<div>
						<label for="email">
							{{i18n[lang]['pages']['register']['email']}}
						</label>
					</div>
					<div>
						<input type="textbox" name="email" />
					</div>
					<div>
						<label for="studentnum">
							{{i18n[lang]['pages']['register']['student_num']}}
						</label>
					</div>
					<div>
						<input type="textbox" name="student_num" />
					</div>
					<div>
						<label for="submit">
							&nbsp;
						</label>
					</div>
					<div>
						<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['submit']}}" />
					</div>
				</form>
%			  end
			</div>
%cinclude parts part=3
</body>
</html>