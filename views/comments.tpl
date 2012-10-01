%			if 'post' in globals():
%			  if post.allow_comments and 'post' in request.path and 'create' not in request.path and 'edit' not in request.path:
				<div id="comments">
%				if post.comments.count() == 0:
					<p class="notice">{{i18n[lang]['post']['nocomments']}}</p>
%				else:
					<ol class="commentlist clearfix">
						<li class="c2">
							<h2>{{post.comments.count()}} Response{{'s' if post.comments.count() > 1 else ''}}</h2>
							<div class="paging">
								<div class="prev"></div>

								<div class="next"></div>
							</div>
						</li>
%					for comment in comments:
%						cinclude comment comment=comment
%					end
%				end
					</ol>
%				if request.logged_in:
					<div id="respond" class="clearfix">
						<h2>{{i18n[lang]['post']['postyourcomment']}}</h2>

						<div class="cancel-comment-reply">
							<small><a rel="nofollow" id="cancel-comment-reply-link" href=
							"/view/post/{{post.id}}#respond" class="c3" name="cancel-comment-reply-link">{{i18n[lang]['post']['cancelreply']}}</a></small>
						</div>

						<form action="/post/view/{{post.id}}/comment" method="post" class="form clearfix">
							<p>{{i18n[lang]['loggedinas']}} <a href="/user/{{request.user.username}}">{{request.user.username}}</a>.
							<a href="/logout" title="{{i18n[lang]['logoutof']}}">{{i18n[lang]['logout']}} &raquo;</a></p>
							<p>
								<label for="comment">{{i18n[lang]['post']['comment_form']['comments']}}</label> 
								<textarea name="comment" id="comment" rows="10" cols="10" tabindex="4" class="tf"></textarea>
							</p>
							<p>
								<label for="submit">&nbsp;</label>
								<input name="submit" type="submit" id="submit" tabindex="5" class="submit" value="{{i18n[lang]['post']['comment_form']['submit']}}" />
							</p>
						</form>
					</div>
%				end
				</div>
%			  end
%			end