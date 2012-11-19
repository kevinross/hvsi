%from hvsi.imports import *
%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
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
%cinclude parts part=3
</body>
</html>