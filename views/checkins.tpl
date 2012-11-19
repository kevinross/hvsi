%from hvsi.imports import *
%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<h2><a href="/user/{{vuser.username}}">{{vuser.username}}</a></h2>
				<h3>{{i18n[lang]['pages'][page]['addcheckin']}}</h3>
				<form action="/user/{{vuser.username}}/checkins/add" method="post">
					{{i18n[lang]['pages'][page]['table']['time']}}: <input type="textbox" class="dt" name="time" />
					{{i18n[lang]['pages'][page]['table']['location']}}: <select name="location">
%						for location in db.locations:
								<option value="{{location}}">{{location}}</option>
%						end
							  </select>
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['add']}}" />
				</form>
				<br/>
				<h3>{{i18n[lang]['pages'][page]['delcheckin']}}</h3>
				<form action="/user/{{vuser.username}}/checkins/delete" method="post">
					<input type="submit" name="submit" value="{{i18n[lang]['pages'][page]['delete']}}" />
					<table border="1" style="width: 100%;">
						<tr>
							%i=i18n[lang]['pages'][page]['table']
							<td><strong>{{i['id']}}</strong></td>
							<td><strong>{{i['location']}}</strong></td>
							<td><strong>{{i['time']}}</strong></td>
							<td><strong>{{i18n[lang]['pages'][page]['delete']}}?</strong></td>
							%del i
						</tr>
%					  for checkin in checkins:
						<tr>
							<td><strong>{{checkin.id}}</strong></td>
							<td>{{checkin.location}}</td>
							<td>{{checkin.time.isoformat()}}</td>
							<td><input type="checkbox" name="{{'checkin_' + str(checkin.id)}}" />
						</tr>
%					  end
					</table>
					<br/>
					<br/>
				</form>
				<script>
				$('.dt').datetimepicker({
					showSecond: true,
					timeFormat: 'hh:mm:ss',
					dateFormat: 'yy-mm-dd'
				});
				</script>
			</div>
%cinclude parts part=3
</body>
</html>