			<div class="section s4">
				<div class="standard tidy">
					<div class="layout a-b content">
%					  if not '/register' in request.path:
						<div class="gr a">
					   			<img src="/img/video.gif" />
						</div>
%					  end
						<div class="gr b s4-b">
                        	<div class="padding">
                           	  <span style="font-size: 2em; color: #555555;">{{i18n[lang]['pages'][page]['title']}}</span><br />
                                {{i18n[lang]['pages'][page]['subtitle']}}
                                <br />
                              <span style="font-size: .6em; color: #777777;">{{i18n[lang]['pages'][page]['blurb']}}</span>
						  </div>
						</div>
					</div>
				</div>
			</div>
