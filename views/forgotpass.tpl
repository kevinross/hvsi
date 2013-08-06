%cinclude part_html_decl
<head>
%	cinclude head
</head>
%cinclude part_html_body
%			  if 'success' in request.params:
					<div><strong>{{i18n[lang]['pages'][page]['success']}}</strong></div>
%			  else:
				<form action="/forgot_password" method="post">
					<div>
						<label for="email">
							{{i18n[lang]['pages']['register']['email']}}
						</label>
					</div>
					<div>
						<input type="textbox" name="email" />
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
%cinclude part_html_sidebar
</body>
</html>
