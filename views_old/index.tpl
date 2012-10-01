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
%					  for post in posts:
%						cinclude post post=post
%					  end
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
