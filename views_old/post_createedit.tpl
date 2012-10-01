%g = globals()
%if 'i18n' not in g:
%	from i18n import i18n
%end
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
	<head>
%		cinclude head
	</head>
	<body class="center">
		<div class="fluid" id="container">
%			cinclude section_s1
%			cinclude section_s2
%			cinclude section_s3
%			cinclude section_s4
	  		<div class="section s5">
%			if error:
				<div class="padding content small">
				  <div class="gr b">
					<span style="font-size: 1em; color: red;">{{i18n[lang][error]}}</span>
				  </div>
				</div>
%			end
				<div class="standard tidy">
					<div class="layout a-b-c content">
%if mode=='edit':
%	action='/post/edit/' + str(post.id)
%	title_e=post.title_e
%	title_f=post.title_f
%	content_e=post.content_e
%	content_f=post.content_f
%else:
%	action='/post/create'
%	title_e=title_f=content_e=content_f=''
%end
						<form action="{{action}}" method="POST">
							<div class="post-title">
								Title (English): <input type="textfield" name="title_e" value="{{title_e}}"/><br/>
								Title (French): <input type="textfield" name="title_f" value="{{title_f}}"/>
							</div><br/>
							<div class="post-content">
								Content (English): <textarea cols="50" rows="10" name="content_e">{{content_e}}</textarea><br/>
								Content (French): <textarea cols="50" rows="10" name="content_f">{{content_f}}</textarea>
							</div><br/>
							<input type="submit" value="{{mode.title()}}"/>
						</form>
					</div>
				</div>
			</div>
			<br/>
			<br/>
			<br/>
%			cinclude section_s6
%			cinclude section_s7
		</div>
	</body>
</html>
