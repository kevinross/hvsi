%from hvsi.imports import *
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