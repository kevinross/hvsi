%cinclude part_html_decl
<head>
%	cinclude head
</head>
%cinclude part_html_body
%				cinclude post template_settings=dict(noescape=True)
%			  if request.path == '/':
%			   for i in range(5):
%				try:
%					cinclude post post=posts[i], template_settings=dict(noescape=True)
%				except:
%					pass
%				end
%			   end
%			  end
%			  if 'view' in request.path:
%				cinclude comments comments=post.comments
%			  end
			</div>
%cinclude part_html_sidebar
</body>
</html>
