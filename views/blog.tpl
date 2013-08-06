%cinclude part_html_decl
<head>
%	cinclude head
</head>
%cinclude part_html_body notitle=True
%			for post in posts:
%				cinclude post template_settings=dict(noescape=True), post=post
%				cinclude comments
%			end
			</div>
%cinclude part_html_sidebar
</body>
</html>
