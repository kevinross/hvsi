%from i18n import i18n
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
	<head>
	<title>
		{{i18n[lang]['pages']['title']}}
	</title>

	<!--[if IE 6]>
	<style type="text/css" media="all">/css/fix-ie-6.css";</style>
	<![endif]-->
	<!--[if IE 7]>
	<style type="text/css" media="all">/css/fix-ie-7.css";</style>
	<![endif]-->
		<LINK href="/css/page-layout.css" rel="stylesheet" type="text/css">
		<LINK href="/css/style.css" rel="stylesheet" type="text/css">
		<LINK href="/css/theme.css" rel="stylesheet" type="text/css">
	</head>


	<body class="center">
		<div class="fluid" id="container">
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
			<div class="section s2">
				<div class="standard tidy">
					<div class="layout a-b content">
						<div class="gr a">
							<div class="padding">
					   			<img src="img/logo.gif" alt="" width="149" height="143" />
							</div>
						</div>
						<div class="gr b s2-b">
							<div class="padding">
								<ul class="s2-ul">
%								  for i in i18n[lang]['hvsi_title']:
									<li>{{i}}</li>
%								  end
								</ul>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="section s3">
				<div style="margin-left: 20px; float: left;">
				  <a href="?setlang={{i18n[lang]['altlang']['key']}}" style="color: white; text-decoration: none;">{{i18n[lang]['altlang']['name']}}</a>
				</div>
				<div class="content">
			<span style="font-weight: bold; color: #aaaaaa; font-size: .9em; text-transform: uppercase;">Twitter:</span> {{twitter}}
				</div>
			</div>
			<div class="section s4">
				<div class="standard tidy">
					<div class="layout a-b content">
%					  if not '/register' in request.path:
						<div class="gr a">
					   			<img src="/img/video.gif" />
						</div>
%					  end
						<div class="gr b s4-b">
                        	<div class="padding">
                           	  <span style="font-size: 2em; color: #555555;">{{i18n[lang]['pages'][page]['title']}}</span><br />
                                {{i18n[lang]['pages'][page]['subtitle']}}
                                <br />
                              <span style="font-size: .6em; color: #777777;">{{i18n[lang]['pages'][page]['blurb']}}</span>
						  </div>
						</div>
					</div>
				</div>
			</div>
	  <div class="section s5">
%if error:
				<div class="padding content small">
				  <div class="gr b">
					<span style="font-size: 1em; color: red;">{{i18n[lang][error]}}</span>
				  </div>
				</div>
%end
				<div class="standard tidy">
					<div class="layout a-b-c content">
					
					  <form action="/register" method="POST">
						<table id="reg_table">
							<tr>
								<td class="gr a"><label for="username">{{i18n[lang]['username']}}:</label></td>
								<td class="gr b"><input type="text" class="login_field textfield" name="username"/></td>
							</tr>
							<tr>
								<td class="gr a"><label for="name">{{i18n[lang]['name']}}:</label></td>
								<td class="gr b"><input type="text" class="login_field textfield" name="name"/></td>
							</tr>
							<tr>
								<td class="gr a"><label for="password">{{i18n[lang]['password']}}:</label></td>
								<td class="gr b"><input type="password" class="login_field textfield" name="password"/></td>
							</tr>
							<tr>
								<td class="gr a"><label for="password_confirm">{{i18n[lang]['password_confirm']}}:</label></td>
								<td class="gr b"><input type="password" class="login_field textfield" name="password_confirm"/></td>
							</tr>
							<tr>
								<td class="gr a"><label for="language">{{i18n[lang]['language']}}:</label><br/>
								<span style="font-size: 0.6em;">{{i18n[lang]['langchange']}}</span></td>
								<td class="gr b"><select name="language"><option value="e">English</option><option value="f">Francais</option></select></td>
							</tr>
							<tr>
								<td class="gr a"><label for="student_num">{{i18n[lang]['student_num']}}:</label></td>
								<td class="gr b"><input type="text" class="login_field textfield" name="student_num"/></td>
							</tr>
							<tr>
								<td class="gr a"><label for="email">{{i18n[lang]['email']}}:</label></td>
								<td class="gr b"><input type="text" class="login_field textfield" name="email"/></td>
							</tr>
							<tr>
								<td class="gr a"><label for="twitter">{{i18n[lang]['twitter']}}:</label><br/>
								<span style="font-size: 0.6em;">{{i18n[lang]['optional_info']}}</span></td></td>
								<td class="gr b"><input type="text" class="login_field textfield" name="twitter"/></td>
							</tr>
							<tr>
								<td class="gr a"><label for="cell">{{i18n[lang]['cell']}}:</label><br/>
								<span style="font-size: 0.6em;">{{i18n[lang]['optional_info']}}</span></td></td>
								<td class="gr b"><input type="text" class="login_field textfield" name="cell"/></td>
							</tr>
							<tr>
								<td class="gr a"/>
								<td class="gr b"><input type="submit" value="{{i18n[lang]['register']}}"/></td>
							</tr>
						</table>
					  </form>
					</div>
				</div>
			</div>
			<br/>
			<br/>
			<br/>
	  <div class="section s6 hide">
				<div class="standard tidy">
					<div class="layout a-b-c content">
						<div class="gr a">
							<div class="padding">
							<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eleifend viverra metus et cursus. Vestibulum suscipit egestas ultricies.  <a href="#">Proin bibendum lectus</a> ullamcorper elit adipiscing ultricies quis sed neque. Donec pretium consectetur urna quis rutrum. Ut venenatis varius velit sed tincidunt. Donec commodo ipsum nec nulla ullamcorper quis tincidunt diam pellentesque. Maecenas augue nisi, gravida et tristique in, pharetra eu ligula. Phasellus venenatis eros ac lacus euismod porta. Vestibulum interdum, ipsum ut congue consequat,  <a href="#">ligula diam</a> hendrerit turpis, ut pulvinar arcu risus id odio. Vestibulum pellentesque tincidunt lacus vitae viverra.</p>
							</div>
						</div>
						<div class="gr b">
							<div class="padding">
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eleifend viverra metus et cursus. Vestibulum suscipit egestas ultricies.  <a href="#">Proin bibendum lectus</a> ullamcorper elit adipiscing ultricies quis sed neque. Donec pretium consectetur urna quis rutrum. Ut venenatis varius velit sed tincidunt. Donec commodo ipsum nec nulla ullamcorper quis tincidunt diam pellentesque. Maecenas augue nisi, gravida et tristique in, pharetra eu ligula. Phasellus venenatis eros ac lacus euismod porta. Vestibulum interdum, ipsum ut congue consequat,  <a href="#">ligula diam</a> hendrerit turpis, ut pulvinar arcu risus id odio. Vestibulum pellentesque tincidunt lacus vitae viverra.</p>
							</div>
						</div>
						<div class="gr c">
							<div class="padding">
														<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eleifend viverra metus et cursus. Vestibulum suscipit egestas ultricies.  <a href="#">Proin bibendum lectus</a> ullamcorper elit adipiscing ultricies quis sed neque. Donec pretium consectetur urna quis rutrum. Ut venenatis varius velit sed tincidunt. Donec commodo ipsum nec nulla ullamcorper quis tincidunt diam pellentesque. Maecenas augue nisi, gravida et tristique in, pharetra eu ligula. Phasellus venenatis eros ac lacus euismod porta. Vestibulum interdum, ipsum ut congue consequat,  <a href="#">ligula diam</a> hendrerit turpis, ut pulvinar arcu risus id odio. Vestibulum pellentesque tincidunt lacus vitae viverra.</p>
							</div>
						</div>
					</div>
					<br class="shim"/>
				</div>
			</div>
			<div class="section s7">
				<div class="content" style="text-align: center;">
					<img src="img/sponsors/hvsi.gif" />
					<img src="img/sponsors/hvsi.gif" />
					<img src="img/sponsors/hvsi.gif" />
					<img src="img/sponsors/hvsi.gif" />
					<img src="img/sponsors/hvsi.gif" />
					<img src="img/sponsors/hvsi.gif" />
					<img src="img/sponsors/hvsi.gif" />
					<img src="img/sponsors/hvsi.gif" />
				</div>
			</div>
		</div>
	</body>
</html>
