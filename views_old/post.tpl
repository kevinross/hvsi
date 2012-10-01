%if 'post' in globals():
							<div class="post-title">
								{{getattr(post, 'title_' + lang)}}
							</div>
							<div class="post-time">
								{{post.time.isoformat()}}
							<div>
							<div class="post-body">
								{{getattr(post, 'content_' + lang)}}
							</div>
%						  if '/post/view' in request.path:
							<div class="post-comments">
%							  for comment in post.comments:
								<div class="post-comment">
									<span class="comment-user">
										{{comment.user.username}}
									</span>
									<span class="comment-content">
										{{comment.content}}
									</span>
								</div>
%							  end
%						  end
%end