<html>
	<head>
		<title>HvsI Initial Configuration</title>
	</head>
	<body>
		<h3>Database Connection</h3>
		<form action="4" method="post">
			Protocol: <select name="dbproto">
					  %if has_mysql:
						<option value="mysql">MySQL</option>
					  %end
						<option value="postgres">Postgres</option>
						<option value="sqlite">SQLite</option>
					  </select><br/><br/>
			Hostname (filepath for SQLite): <input type="text" name="dbhost" /><br/><br/>
			Username: <input type="text" name="dbuser" /><br/><br/>
			Password: <input type="text" name="dbpass" /><br/><br/>
			Database (filename for SQLite): <input type="text" name="dbdb" /><br/><br/>
			<input type="submit" value="Next" />
		</form>
	</body>
</html>