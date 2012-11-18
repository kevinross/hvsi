<html>
	<head>
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
		<title>HvsI Initial Configuration</title>
	</head>
	<body>
		<h3>Basic Parameters</h3>
		<form action="2" method="post">
			Hostname: <input type="textfield" name="host" /><br/><br/>
			Static Content Host: <input type="radio" id="builtin" name="statichost" value="builtin" checked>Built-in</input>
								 <input type="radio" id="external" name="statichost" value="external">External:</input>
								 <input type="textfield" id="externalhost" name="externalhost" disabled="true"/><br/><br/>
			Debug Mode: <input type="radio" name="debug" value="yes">On</input>
						<input type="radio" name="debug" value="no" checked>Off</input><br/><br/>
			<input type="submit" value="Next" />
		</form>
		<script>
			$('input:radio').change(function(evt) {
				if (this.value == "builtin") {
					$('#externalhost').prop('disabled', true);
				} else {
					$('#externalhost').prop('disabled', false);
				}
			});
		</script>
	</body>
</html>