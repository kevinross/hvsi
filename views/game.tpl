%from imports import *
%cinclude parts part=1
<head>
%	cinclude head
	<style>
		table {
			width: 350px;
		}
		tr {
			height: 40px;
		}
		td {
			border: 1px solid;
		}
	</style>
</head>
%cinclude parts part=2
				<h2>{{i18n[lang]['pages'][page]['title']}}</h2>
				<table>
				<tr>
				<td>
				<form action="/game" method="post">
%				  if db.Game.is_started:
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['end']}}" />
%				  else:
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['start']}}" />
%				  end
				</form>
				</td>
				<td>
				<form action="/reg" method="post">
%				  if db.Game.is_reg:
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['endr']}}" />
%				  else:
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['startr']}}" />
%				  end
				</form>
				</td>
				</tr>
				<tr>
				<td>
				<form action="/count" method="post">
%				  if db.Game.is_countdown:
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['discount']}}" />
%				  else:
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['encount']}}" />
%				  end
				</form>
				</td>
				<td>
				<form action="/count_time" method="post">
					Countdown To: <input type="textfield" class="dt" id="count_time" name="count_time" value="{{str(db.Game.countdown_time)}}" />
				</td>
				<td>
				<input type="submit" name="submit" value="Save" />
				</td>
				</form>
				</tr>
				<tr>
				<form action="/startend" method="post">
					<td>Game Start: <input type="textfield" class="dt" id="start_time" name="start_time" value="{{str(db.Game.game_start)}}" /></td>
					<td>Game End: <input type="textfield" class="dt" id="end_time" name="end_time" value="{{str(db.Game.game_end)}}" /></td>
					<td><input type="submit" name="submit" value="Save" /></td>
				</form>
				</tr>
				<tr>
				<form action="/rego" method="post">
					<td>Registration Cutoff:</td><td><input type="textfield" class="dt" id="rego" name="rego" value="{{str(db.Game.game_rego)}}" /></td>
					<td><input type="submit" name="submit" value="Save" /></td>
				</form>
				</tr>
				<tr>
				<form action="/hrsbc" method="post">
					<td>Hours Between Checkins:</td><td><input type="textfield" id="hrsbc" name="hrsbc" value="{{str(db.Game.hours_between_checkins)}}" /></td>
					<td><input type="submit" name="submit" value="Save" /></td>
				</form>
				</tr>
				<tr>
				<form action="/itemail" method="post">
					<td>IT Email:</td><td><input type="textfield" id="itemail" name="itemail" value="{{str(db.Game.it_email)}}" /></td>
					<td><input type="submit" name="submit" value="Save" /></td>
				</form>
				</tr>
				</table>
				<script>
				$('.dt').datetimepicker({
					showSecond: true,
					timeFormat: 'hh:mm:ss',
					dateFormat: 'yy-mm-dd'
				});
				</script>
				<br/>
				<a href="/email">Send Email</a>
				<br/>
			</div>
%cinclude parts part=3
</body>
</html>