%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2, nologin=True, nocontent=True
		<div id="content">
			<div id="left">
				<h1>{{i18n[lang]['pages'][page]['title']}}</h1>
%				if bottle.request.session.error:
					<div style="color: red;">
						{{i18n[lang]['pages'][page][bottle.request.session.error]}}
					</div>
%				    bottle.request.session.error = None
%				end
%				if bottle.request.session.data:
%					data = bottle.request.session.data_dict
%				else:
%					data = dict()
%				end
				<h3>{{i18n[lang]['pages'][page]['userinfo']}}</h3>
				<form action="/register" method="post">
%				for i in [('username','textbox'), \
%						  ('name','textbox'), \
%						  ('password','password'), \
%						  ('password_confirm','password')]:
					<div class="form_label">
					  <label for="{{i[0]}}">
						{{i18n[lang]['pages'][page][i[0]]}}:
					  </label>
					</div>
					<div class="form_field">
						<input type="{{i[1]}}" id="{{i[0]}}" name="{{i[0]}}" value="{{data.get(i[0], '')}}"/>
						<span class="extra_info">({{i18n[lang]['pages'][page]['required']}})</span>
					</div>
%				end
					<div class="form_label">
					  <label for="language">
					    Language:
					  </label>
					</div>
					<div class="form_field">
						<select id="language" name="language">
%						  for l in i18n.keys():
							<option value="{{l}}" {{'selected' if data.get('language','') == l else ''}}>{{i18n[l]['lang']}}</option>
%						  end
						</select>
						<span class="extra_info">({{i18n[lang]['pages'][page]['changedlater']}})</span>
					</div>
%				for i in [('student_num','textbox',i18n[lang]['pages'][page]['required']), \
%						  ('email','textbox',i18n[lang]['pages'][page]['required']), \
%						  ('twitter','textbox',i18n[lang]['pages'][page]['optional']), \
%						  ('cell','textbox',i18n[lang]['pages'][page]['optional'])]:
					<div class="form_label">
					  <label for="{{i[0]}}">
						{{i18n[lang]['pages'][page][i[0]]}}:
					  </label>
					</div>
					<div class="form_field">
						<input type="{{i[1]}}" id="{{i[0]}}" name="{{i[0]}}" value="{{data.get(i[0], '')}}"/>
%					  if i[2]:
						<span class="extra_info">({{i[2]}})</span>
%					  end
					</div>
%				end
					<br/>
                    <h3>{{i18n[lang]['pages'][page]['human?']}}</h3>
                    <div class="form_label">
                        <label for="answer">
                            {{SkillTestingQuestion(data['question']).question(lang)}}
                        </label>
                    </div>
                    <div class="form_field">
                        <input type="textbox" id="answer" name="answer" value=""/>
                    </div>
                    <br/>
					<h3>{{i18n[lang]['pages'][page]['eula']}}</h3>
					<div class="eula">
						<span>
							<input type="checkbox" name="liability" />
							{{i18n[lang]['pages'][page]['liability']}} <a href="/pdf/liability.pdf">{{i18n[lang]['pages'][page]['liabilitywaiver']}}</a>
						</span>
						<br/>
						<span>
							<input type="checkbox" name="safety" />
							{{i18n[lang]['pages'][page]['safety']}} <a href="/pdf/safety.pdf">{{i18n[lang]['pages'][page]['safetyrules']}}</a>
						</span>
					</div>
					<div class="form_field">
						<br/>
						<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['register']}}" />
					</div>
				</form>
				<br/>
				<br/>
				<br/>
			</div>
%cinclude parts part=3
</body>
</html>
