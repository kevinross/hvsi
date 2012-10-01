%if 'i18n' not in globals():
	%from i18n import i18n
%end
%import calendar
%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<h2>Cure #{{cure.id}}</h2>
				<form action="/cures/edit/{{cure.id}}" method="post">
					<div>
						<label for="time">
							{{i18n[lang]['pages']['cures']['table']['time']}}
						</label>
					</div>
					<div>
						<input type="textbox" name="time" value="{{'' if not cure.time else cure.time.isoformat()}}" />
					</div>
					<div>
						<label for="card_id">
							{{i18n[lang]['pages']['cures']['table']['cardid']}}
						</label>
					</div>
					<div>
						<input type="textbox" name="card_id" readonly="1" value="{{'' if not cure.card_id else cure.card_id}}" />
					</div>
					<div>
						<label for="used">
							{{i18n[lang]['pages']['cures']['table']['used']}}
						</label>
					</div>
					<div>
						<input type="checkbox" name="used" {{'checked="1"' if cure.used else ''}} />
					</div>
					<div>
						<label for="username">
							{{i18n[lang]['pages']['register']['username']}}
						</label>
					</div>
					<div>
						<input type="textbox" name="username" value="{{'' if not cure.player else cure.player.username}}" />
					</div>
					<div>
						<label for="disqualified">
							{{i18n[lang]['pages']['cures']['table']['disqualified']}}
						</label>
					</div>
					<div>
						<input type="checkbox" name="disqualified" {{'checked="1"' if cure.disqualified else ''}} />
					</div>
					<div>
						<label for="submit">
							&nbsp;
						</label>
					</div>
					<div>
						<input type="submit" name="submit" value="{{i18n[lang]['pages']['user']['edit']}}" />
					</div>
				</form>
				<br/>
			</div>
%cinclude parts part=3
</body>
</html>