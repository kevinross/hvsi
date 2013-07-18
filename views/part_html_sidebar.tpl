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
				function fixup_corners() {
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
				}}
                fixup_corners();
	//]]>
	</script>
%  if not hasattr(request, 'logged_in') or (hasattr(request, 'logged_in') and (not request.logged_in or request.player)):
	%include analytics
%  end