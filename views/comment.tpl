						<li class="comment byuser comment-author-admin bypostauthor even thread-even depth-1" id="comment-{{comment.id}}">
							<div class="comment-body">
								<div class="comment-author vcard">
									<cite class="fn">{{comment.user.name}} ({{comment.user.username}})</cite> <span class="says">:</span>
								</div>

								<div class="comment-meta commentmetadata">
									<a href="/post/{{comment.post.id}}#comment-{{comment.id}}">
									{{calendar.month_name[comment.time.month]}} {{comment.time.day}}, {{comment.time.year}} @ {{comment.time.strftime('%H:%M')}}</a>&nbsp;&nbsp;
								</div>

								<p>{{comment.content}}</p>
%							if request.logged_in:
								<div class="reply">
									<a rel='nofollow' class='comment-reply-link' href='#respond'>{{i18n[lang]['post']['comment']['reply']}}</a>
								</div>
%end
							</div>
						</li>