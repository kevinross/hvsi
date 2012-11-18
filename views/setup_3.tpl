<html>
	<head>
		<title>HvsI Initial Configuration</title>
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
	</head>
	<body>
		<h3>Exception Logging</h3>
		<form action="3" method="post">
			Type: <input type="radio" class="type" id="file" name="exceptions" value="file" checked>Files</input>
			<input type="radio" class="type" id="email" name="exceptions" value="email">Email</input>
			<input type="radio" class="type" id="both" name="exceptions" value="both">Both</input>
			<br/><br/>
			<h4>Files Configuration</h4>
			Folder for exception reports:<input type="text" class="file" name="file" />
			<br/><br/>
			<h4>Email Configuration</h4>
			To Address: <input type="text" class="email" name="to" disabled/><br/>
			From Address: <input type="text" class="email" name="from" disabled/><br/>
			Server: <input type="text" class="email" name="server" disabled/><br/>
			Username: <input type="text" class="email" name="username" disabled/><br/>
			Password: <input type="text" class="email" name="password" disabled/><br/>
			<br/><br/>
			<input type="submit" value="Next" />
		</form>
		<script type="text/javascript">
			$('input:radio.type').change(function(evt) {
				if (this.value == "file") {
					$('.email').prop('disabled', true);
					$('.file').prop('disabled', false);
				} else {
					$('.email').prop('disabled', false);
					$('.file').prop('disabled', this.value == "email");
				}
			});
		</script>
	</body>

</html>