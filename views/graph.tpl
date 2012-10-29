%if 'i18n' not in globals():
	%from i18n import i18n
%end
%import calendar, database as db, datetime
%cinclude parts part=1
<head>
%	cinclude head
	<script type="text/javascript" src="http://www.google.com/jsapi"></script>
	<script type="text/javascript">
	  google.load('visualization', '1', {packages: ['corechart']});
	</script>
	<script type="text/javascript">
		function drawVisualization() {
			// Create and populate the data table.
			var data = new google.visualization.DataTable();
			data.addColumn('string', '{{i18n[lang]['pages'][page]['time']}}');
			data.addColumn('number', '{{i18n[lang]['sidebar']['status']['zombies']}}');
			data.addColumn('number', '{{i18n[lang]['sidebar']['status']['humans']}}');
			// The day graph
%		  n = datetime.datetime.now()
%		  twelve_ago = n - datetime.timedelta(0,0,0,0,0,22)
%		  hours = [twelve_ago + datetime.timedelta(0,0,0,0,0,x) for x in range(0,22)]
%		  for h in hours:
%			events = db.Snapshot.points_before_date(h)
%			if events.count() > 0:
%				event = events[0]
%			else:
%				event = None
%			end
			data.addRow(['{{h.hour}}:00', {{'null' if not event else event.num_zombies}}, {{'null' if not event else event.num_humans}}]);
%		  end
			var begin_data = new google.visualization.DataTable();
			begin_data.addColumn('string', '{{i18n[lang]['pages'][page]['time']}}');
			begin_data.addColumn('number', '{{i18n[lang]['sidebar']['status']['zombies']}}');
			begin_data.addColumn('number', '{{i18n[lang]['sidebar']['status']['humans']}}');
%		  monday = db.Game.game_start - datetime.timedelta(0, 0, 0, 0, 30, 1)
%		  friday = db.Game.game_end + datetime.timedelta(0, 0, 0, 0, 30, 1)
%		  dates = []
%		  d = monday
%		  while d <= friday:
%			dates.append(d)
%			d = d + datetime.timedelta(hours=4)
%		  end
%		  dates.append(d+datetime.timedelta(hours=4))
%		  for h in dates:
%			events = db.Snapshot.points_before_date(h)
%			if events.count() > 0 and h <= n:
%				event = events[0]
%			else:
%				event = None
%			end
			begin_data.addRow(['Nov {{h.day}} {{h.hour}}:00', {{'null' if not event else event.num_zombies}}, {{'null' if not event else event.num_humans}}]);
%		  end
			var top_data = new google.visualization.DataTable();
%			top_ten = ','.join(['["' + x.player.username + '",' + str(x.kills) + ']' for x in db.Score.top[0:10]])
			var players = [{{!top_ten}}];
			top_data.addColumn('string', '{{i18n[lang]['player_status']['zombie']}}');
			top_data.addColumn('number', '{{i18n[lang]['pages'][page]['count']}}');
			top_data.addRows(players.length);
			for (var i = 0; i < players.length; i++) {
				top_data.setValue(i, 0, players[i][0]);
			}
			for (var i = 0; i < players.length; i++) {
				top_data.setValue(i, 1, players[i][1]);
			}
			var top_chart = new google.visualization.BarChart(
				document.getElementById('top_zombies'));
			top_chart.draw(top_data, {title: '{{i18n[lang]['pages'][page]['topzombies']}}',
						 legend: 'none',
						 width: 500, height: 400,
						 vAxis: {title: "{{i18n[lang]['player_status']['zombie']}}"},
						 hAxis: {title: "{{i18n[lang]['pages'][page]['count']}}"}});
									  
			// Create and draw the visualization.
			var chart = new google.visualization.LineChart(
				document.getElementById('day_visualization'));
			chart.draw(data, {title: '{{i18n[lang]['pages'][page]['zombiecount24']}}',
						  width: 500, height: 400,
						  vAxis: {title: "{{i18n[lang]['pages'][page]['player']}}"},
						  hAxis: {title: "{{i18n[lang]['pages'][page]['time']}}"}}
				  );
			var week_chart = new google.visualization.LineChart(
				document.getElementById('week_visualization'));
			week_chart.draw(begin_data, {title: '{{i18n[lang]['pages'][page]['zombiecountw']}}',
						  width: 500, height: 400,
						  vAxis: {title: "{{i18n[lang]['pages'][page]['player']}}"},
						  hAxis: {title: "{{i18n[lang]['pages'][page]['time']}}"}}
				  );
			
			// The daily graph
		}

  		google.setOnLoadCallback(drawVisualization);
	</script>
</head>
%cinclude parts part=2
				<div id="top_zombies"></div><br/>
				<div id="day_visualization" style="width: 500px; height: 400px;"></div><br/>
				<div id="week_visualization" style="width: 500px; height: 400px;"></div>
			</div>
%cinclude parts part=3
</body>
</html>
