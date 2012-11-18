<html>
	<head>
		<title>HvsI Initial Configuration</title>
	</head>
	<body>
		%if not failed:
		<p>Congratulations, you have already installed all required dependencies!</p>
		<p>Click <a href="2">Next</a> to configure basic sitewide parameters.</p>
		%else:
		<p>You are missing the following python modules: {{', '.join(failed)}}</p>
		This wizard can attempt to install them for you in {{path}} by clicking
			<form action="1.5" method="post" style="display:inline!important;"><input type="submit" value="here" /></form>
		%end
	</body>
</html>