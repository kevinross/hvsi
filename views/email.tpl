%if 'i18n' not in globals():
	%from i18n import i18n
%end
%import calendar
%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<h2>Send Email to Players</h2>
				<form action="/email" method="post">
					<div>
						<label for="from">
							From:
						</label>
					</div>
					<div>
						<input type="textbox" name="from" />
					</div>
					<div>
						<label for="password">
							Password:
						</label>
					</div>
					<div>
						<input type="password" name="password" />
					</div>
					<div>
						<label for="target">
							Target:
						</label>
					</div>
					<div>
						<select name="target">
							<option value="humans">Humans</option>
							<option value="zombies">Zombies</option>
							<option value="active">Active Players</option>
							<option value="inactive">Inactive Players</option>
							<option value="all">All Players</option>
						</select>
					</div>
					<div>
						<label for="subject">
							Subject:
						</label>
					</div>
					<div>
						<input type="textbox" name="subject">
					</div>
					<div>
						<label for="msg">
							Content:
						</label>
					</div>
					<div>
						<textarea rows="20" cols="70" name="msg"></textarea>
					</div>
					<div>
						<label for="submit">
							&nbsp;
						</label>
					</div>
					<div>
						<input type="submit" name="submit" value="Email" />
					</div>
				</form>
				<br/>
				<br/>
			</div>
%cinclude parts part=3
</body>
</html>