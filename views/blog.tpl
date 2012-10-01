%if 'i18n' not in globals():
	%from i18n import i18n
%end
%import calendar
%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
%			for post in posts:
%				cinclude post template_settings=dict(noescape=True), post=post
%				cinclude comments
%			end
			</div>
%cinclude parts part=3
</body>
</html>