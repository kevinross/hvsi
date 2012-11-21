%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<h1>{{i18n[lang]['pages'][page]['title']}}</h1>
				<form action="/eula" method="post">
					<div class="eula">
						<span>
							<input type="checkbox" name="liability" />
							{{i18n[lang]['pages']['register']['liability']}} <a href="/eula/liability.pdf">{{i18n[lang]['pages']['register']['liabilitywaiver']}}</a>
						</span>
						<br/>
						<span>
							<input type="checkbox" name="safety" />
							{{i18n[lang]['pages']['register']['safety']}} <a href="/eula/safety.pdf">{{i18n[lang]['pages']['register']['safetyrules']}}</a>
						</span>
					</div>
					<div>
						<label for="submit">
							&nbsp;
						</label>
					</div>
					<div>
						<input type="submit" value="{{i18n[lang]['pages'][page]['agree']}}" />
					</div>
				</form>
			</div>
%cinclude parts part=3
</body>
</html>
