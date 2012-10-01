	  		<div class="section s1">
				<div class="standard tidy">
					<div class="layout b-c content">
%					  if request.logged_in:
						<div class="gr c" style="padding-top: 3px;">
							<a href="/user/{{user.username}}">{{user.name}} ({{user.username}})</a>
							<span style="padding: 0px 10px 0px 10px;">|</span>
							<a href="/logout">{{i18n[lang]['logout']}}</a>
						</div>
%					  else:
                        <form action="/login" method="POST" id="login_form">
                        	<input type="submit" class="login_submit" value="Login"/>
							<div class="gr c">
								Username:<input type="text" class="s1-textfield login_field" name="username"/>
								Password:<input type="password" class="s1-textfield login_field" name="password"/>
							</div>
					  	</form>
%					   end-->
					</div>
				</div>
			</div>
