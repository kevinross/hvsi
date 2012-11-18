<html>
	<head>
		<title>HvsI Initial Configuration</title>
	</head>
	<body>
		%if failed:
		<p>Failed to install modules: {{', '.join(failed)}}, please install these modules manually before continuing.</p>
		%else:
		<p>Congratulations, all modules installed correctly.  Proceed to <a href="2">configure</a> basic sitewide parameters</p>
		%end
	</body>
</html>