%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
%			if request.session.data:
%				data = simplejson.loads(request.session.data)
%				request.session.data = None
%			else:
%				data = dict()
%			end
				<h2>Send Email to Players</h2>
				<form action="/email" method="post">
					<div>
						<label for="from">
							From:
						</label>
					</div>
					<div>
						<input type="textbox" name="from" value="{{data.get('from','')}}"/>
					</div>
					<div>
						<label for="target">
							Target:
						</label>
					</div>
					<div>
						<select name="target">
%						  for i in ['humans','zombies','actives','inactives','all']:
							<option value="{{i}}" {{"selected" if data.get('target','') == i else ''}}>{{i.capitalize()}}</option>
%						  end
						</select>
					</div>
					<div>
						<label for="subject">
							Subject:
						</label>
					</div>
					<div>
						<input type="textbox" name="subject" value="{{data.get('subject','')}}">
					</div>
					<div>
						<label for="msg">
							Content:
						</label>
					</div>
					<div>
						<textarea rows="20" cols="70" name="msg">{{data.get('msg','')}}</textarea>
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
