<html>
	<head>
		<title>HvsI Initial Configuration</title>
	</head>
	<body>
		<h3>Language Setup</h3>
		<p>This step will create copies of the english strings file for you to modify for each language.</p>
		<p>If you already have already created files for each supported language, simply click Save.</p>
		<strong>Languages:</strong>
		<ul>
			%for lang in langs:
			<li>{{lang}}</li>
			%end
		</ul>
		<br/>
		<form action="4.u" method="post">
			Code: <input type="textfield" name="lang_short" />
			<input type="submit" value="Add" />
		</form>
		<br/><br/>
		<form action="4" method="post">
			  <input type="submit" value="Save" />
		</form>
	</body>
</html>