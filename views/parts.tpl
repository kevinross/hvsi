%admin = bottle.request.admin or bottle.request.station
%path = re.match(r'/log[inout]*(.*)', bottle.request.path)
%count = db.Game.is_countdown
%if (not admin and count and not path):
%bottle.redirect('/', 302)
%end
%if part==1:
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
%elif part==2:
<body id="mainBody">
	<div id="pagewidth" class="clearfix">
		<div id="header">
			<div class="logo">
				<a href="/"></a>
			</div>
%if 'nologin' not in globals() or ('nologin' in globals() and not nologin):
		  <div id="loginheader" style="float: right;">
%		  if not hasattr(request, 'logged_in') or (hasattr(request, 'logged_in') and not request.logged_in):
			<a style="float: right;" href="/password_reset">{{i18n[lang]['pass']}}</a>
			<br/>
%		  end
%		cinclude login_header
		  </div>
%end
%		cinclude navigation
		</div>
%if not ('nocontent' in globals() and nocontent):
		<div id="content">
			<div id="left">
              %if get('title', i18n[lang]['pages'][page]['title']):
                <h1>{{get('title', i18n[lang]['pages'][page]['title'])}}</h1>
              %end
%			  if bottle.request.session.error:
				<div style="color: red;">
%if 'suberror' in globals() and suberror:
					{{i18n[lang]['pages'][page][bottle.request.session.error] % i18n[lang]['pages'][page][suberror]}}
%else:
					{{i18n[lang]['pages'][page][bottle.request.session.error]}}
%end
				</div>
				<br/>
%				bottle.request.session.error = None
%			  end
%end
% elif part==3:
			<div id="right">
%				cinclude sidebar
				<div id="creditsfix"></div>
			</div>
		</div>

		<div id="footer"><div style="margin-left: auto; margin-right: auto; width: 200px;"><a href="mailto:{{db.Game.it_email}}">Questions, comments, or concerns?</a></div></div>
	</div>
	<script type="text/javascript" src="{{static('/js/jquery.corner.js')}}"></script>
	<script type="text/javascript">
//<![CDATA[
				//Cufon.replace('#navigation a');
				//Cufon.replace('h1, h2, h3, h4, h5, h6');
				
				if(jQuery.browser.msie)
						$('#mainBody').addClass('ie'+parseInt(jQuery.browser.version));
				else if(jQuery.browser.opera)
						$('#mainBody').addClass('opera');
				
				if(!jQuery.browser.msie && !jQuery.browser.opera)
				{
						$('.comment-body, #respond, .post .postinfo').each(function () {
								$(this).corner('10px');
						});
						
						$('li.comment .reply a, .post a.more-link, .paging a, #comments #respond .form #submit, .wp-pagenavi *').each(function () {
								$(this).corner('5px');
						});
						
						$('.post .postinfo ul.tags li a').each(function () {
								$(this).corner('2px');
						});
				}
	//]]>
	</script>
%  if not hasattr(request, 'logged_in') or (hasattr(request, 'logged_in') and (not request.logged_in or request.player)):
	%include analytics
%  end
%end
