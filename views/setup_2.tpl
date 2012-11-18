<html>
	<head>
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
		<title>HvsI Initial Configuration</title>
	</head>
	<body>
		<h3>Basic Parameters</h3>
		<form action="2" method="post">
			Hostname: <input type="text" name="host" /><br/><br/>
			Static Content Host: <input type="radio" class="host" id="builtin" name="statichost" value="builtin" checked>Built-in</input>
								 <input type="radio" class="host" id="external" name="statichost" value="external">External:</input>
								 <input type="text" id="externalhost" name="externalhost" disabled="true"/><br/><br/>
			Debug Mode: <input type="radio" name="debug" value="yes">On</input>
						<input type="radio" name="debug" value="no" checked>Off</input><br/><br/>
			Exception Logs Directory: <input type="text" name="exceptionlogs" /><br/><br/>
			Timezone: <select name="timezone">
						%try:
						% import pytz
						% zones = pytz.common_timezones
						%except:
						% zones = ['America/Toronto']
						%end
						%for zone in zones:
						<option value="{{zone}}" {{'selected' if zone=='America/Toronto' else ''}}>{{zone}}</option>
						%end
					  </select><br/><br/>
			<input type="submit" value="Next" />
		</form>
		<script type="text/javascript">
			$('input:radio.host').change(function(evt) {
				if (this.value == "builtin") {
					$('#externalhost').prop('disabled', true);
				} else {
					$('#externalhost').prop('disabled', false);
				}
			});
		</script>
	</body>
</html>