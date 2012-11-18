<html>
	<head>
		<title>HvsI Initial Configuration</title>
	</head>
	<body>
		<h3>Database Connection</h3>
		<form action="3" method="post">
			Protocol: <select name="dbproto">
					  %if has_mysql:
						<option value="mysql">MySQL</option>
					  %end
						<option value="postgres">Postgres</option>
						<option value="sqlite">SQLite</option>
					  </select><br/><br/>
			Hostname (filepath for SQLite): <input type="textfield" name="dbhost" /><br/><br/>
			Username: <input type="textfield" name="dbuser" /><br/><br/>
			Password: <input type="textfield" name="dbpass" /><br/><br/>
			Database (filename for SQLite): <input type="textfield" name="dbdb" /><br/><br/>
			<input type="submit" value="Next" />
		</form>
	</body>
</html>