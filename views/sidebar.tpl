%import random, string, database as db
				<ul id="sidebar">
					<li class="widget">
%			s=i18n[lang]['sidebar']['status']
						<h2>{{s['title']}}</h2>
						<h3>{{s['subtitle']}}</h3>
						<ul>
%						if request.logged_in:
							<li><span class="sidebar_key">Username:</span> <span class="sidebar_value">{{request.user.username}}</span></li>
%						  if request.player:
							<li><span class="sidebar_key">Game ID:</span> <span class="sidebar_value">{{request.user.game_id}}</li>
							<li><span class="sidebar_key">Status:</span> <span class="sidebar_value">{{request.user.state.title()}}</li>
%						  end
%						  if request.player and request.user.is_zombie():
%							d=request.user.last_death
%						   if started:
							<li>
								<span class="sidebar_key">{{s['regtag']}}:</span>
								<span class="sidebar_value">
									<form action="/tag" method="post">
										<input type="textbox" name="taggee"/>
										<input type="hidden" name="uid" value="webform_{{''.join(random.sample(string.ascii_letters+string.digits, 36))}}" />
										<input type="submit" style="display:none;" value="Kill"/>
									</form>
								</span>
							</li>
%						  end
							<li><span class="sidebar_key">{{s['died']}}:</span>
								<span class="sidebar_value">
%								  if d and not request.user.zero:
									{{i18n[lang]['days'][d.time.weekday()]}} @ {{d.time.hour}}:{{('0' + str(d.time.minute)) if len(str(d.time.minute)) == 1 else str(d.time.minute)}}
									  {{s['by']}} {{d.tagger.username}}
%								  elif request.user.zero:
								    {{i18n[lang]['sidebar']['status']['zero']}}
%								  end
								</span>
							</li>
							<li><span class="sidebar_key">{{s['kills']}}:</span> <span class="sidebar_value">{{request.user.kills.count()}}</span></li>
%						  elif request.player and request.user.is_human():
%						   d=request.user.last_cure
%						   if d:
							<li><span class="sidebar_key">{{s['cured']}}:</span>
								<span class="sidebar_value">
									{{calendar.day_name[d.time.weekday()]}} @ {{d.time.hour}}:{{('0' + str(d.time.minute)) if len(str(d.time.minute)) == 1 else str(d.time.minute)}}
								</span>
							</li>
%						   end
%						   if not request.user.did_webcheckin:
							<li><span class="sidebar_key"><a href="/webcheckin">{{i18n[lang]['pages']['webcheckin']['title']}}</a></li>
%						   end
%						  end
%						  if hasattr(request, 'admin') and (request.admin or request.station):
							<li><span class="sidebar_key">{{s['used_cures']}}:</span> <span class="sidebar_value">{{db.Cure.used_cards.count()}}</span></li>
							<li><span class="sidebar_key">{{s['unused_cures']}}:</span> <span class="sidebar_value">{{db.Cure.unused_cards.count()}}</span></li>
%						  end
%						end
							<li><span class="sidebar_key">{{s['humans']}}:</span> <span class="sidebar_value">{{db.Player.humans.count()}}</span></li>
							<li><span class="sidebar_key">{{s['zombies']}}:</span> <span class="sidebar_value">{{db.Player.zombies.count()}}</span></li>
%						  if hasattr(request, 'admin') and (request.admin):
							<li><span class="sidebar_key">{{s['users']}}:</span> <span class="sidebar_value">{{db.Player.users.count()}}</span></li>
%						  end
						</ul>
					</li> 
%				  if hasattr(request, 'admin') and (request.admin or request.station):
					<li class="widget">
%			s=i18n[lang]['sidebar']['controls']
						<h2>{{s['title']}}</h2>
						<h3>{{s['subtitle']}}</h3>
						<ul>
%						  if hasattr(request, 'admin') and request.admin:
							<li><span class="sidebar_key"><a href="/post/create">{{i18n[lang]['pages']['post_create']['title']}}</a></span></li>
							<li><span class="sidebar_key"><a href="/users">{{s['userlist']}}</a></span></li>
							<li><span class="sidebar_key"><a href="/cures">{{s['curelist']}}</a></span></li>
							<li><span class="sidebar_key"><a href="/tags">{{s['taglist']}}</a></span></li>
%						  end
							<li><span class="sidebar_key"><a href="/station">{{s['station']}}</a></span></li>
						</ul>
					</li>
%				  end
					<li class="widget">
%						cinclude twitter template_settings=dict(noescape=True)
					</li>
				</ul>
