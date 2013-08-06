%cinclude part_html_decl
<head>
%	cinclude head
</head>
%cinclude part_html_body
				<h2>Cure #{{cure.id}}</h2>
				<form action="/cures/edit/{{cure.id}}" method="post">
					<div>
						<label for="expiry">
							{{i18n[lang]['pages']['cures']['table']['expiry']}}
						</label>
					</div>
					<div>
						<input type="textbox" name="expiry" class="dt" value="{{'' if not cure.expiry else cure.expiry.isoformat()}}" />
					</div>
					<div>
						<label for="time">
							{{i18n[lang]['pages']['cures']['table']['time']}}
						</label>
					</div>
					<div>
						<input type="textbox" name="time" class="dt" value="{{'' if not cure.time else cure.time.isoformat()}}" />
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
						<input type="submit" name="submit" value="{{i18n[lang]['pages']['user_view']['edit']}}" />
					</div>
				</form>
				<br/>
			</div>
%cinclude part_html_sidebar
</body>
</html>
