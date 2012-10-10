%from imports import *
<html>
<head>
<title>
{{i18n[lang]['pages'][page]['title']}}
</title>
<link href='http://fonts.googleapis.com/css?family=Wire+One' rel='stylesheet' type='text/css'>
<style type = "text/css">

body{
	background:url("{{static('/css/images/Countdown.jpg')}}");
	text-align:center;
}
p{
	color:white;
	font-family:'Wire One', sans-serif;
	font-size:1000%;
	margin:0px;
}
#time_div{
	margin-top:150px;
	margin-left:auto;
	margin-right:auto;
	min-width:460px;
	min-height:200px;
	background:rgba(0, 0, 0, 0.81);
	border: solid 1px black;
}
</style>
</head>
	<body>
		<div id ="time_div">
			<p id = "time"> Coming Soon </p>
		</div>
		<script type="text/javascript">
			window.setInterval(function update()
						{
							var currentTime = new Date();
							// "Oct 29 2012 00:00:01"
							//  %b %d %Y %H:%M:%S
							var gameStart = new Date('{{db.Game.countdown_time.strftime("%b %d %Y %H:%M:%S")}}');
							var days = Math.floor((gameStart.getTime() - currentTime.getTime()) / (1000 * 60 * 60 * 24));																								   
							var hours = Math.floor((gameStart.getTime()-currentTime.getTime())/(1000*60*60))-((days)*24);																		       
							var minutes = Math.floor((gameStart.getTime()-currentTime.getTime())/(1000*60))-((hours)*60)-((days)*24*60);						           
							var seconds = Math.floor((gameStart.getTime()-currentTime.getTime())/1000)-(minutes*60)-(hours* 60 * 60) - (days  * 24 * 60 * 60); 
							days=(days<10)?"0"+days:days;
							hours=(hours<10)?"0"+hours:hours;
							minutes=(minutes<10)?"0"+minutes:minutes;
							seconds=(seconds<10)?"0"+seconds:seconds;
							var elem= document.getElementById('time');
							elem.innerHTML=days+":"+hours+":"+minutes+":"+seconds;
						}, 1000);
        </script>
	</body>
</html>
