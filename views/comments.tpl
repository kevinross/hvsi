%			if 'post' in globals():
%			  if 'api' in request.path or (post.allow_comments and 'post' in request.path and 'create' not in request.path and 'edit' not in request.path):
				<div id="comments">
%				if post.comments.count() == 0:
					<p id="nocomment_notice" class="notice">{{i18n[lang]['post']['nocomments']}}</p>
%				else:
					<ol id="commentlist" class="commentlist clearfix">
						<li class="c2">
							<h2><span id="comment_count">{{post.comments.count()}}</span> Response{{'s' if post.comments.count() > 1 else ''}}</h2>
							<div class="paging">
								<div class="prev"></div>

								<div class="next"></div>
							</div>
						</li>
%					for comment in post.comments:
%						cinclude comment comment=comment
%					end
					</ol>
%				end

%				if request.logged_in:
                    <script>
                        function do_comment() {
                            if ($('#nocomment_notice').text() != '') {
                                return true;
                            }
                            $('#comment_form :input').attr('disabled', true);
                            var post = {"one":true,"sqlref":{"name":"Post","items":[parseInt('{{post.id}}')]}};
                            //try {
                                API().blog.add_comment.async(post, $('#comment').val(), function(result) {
                                        $(result).hide().appendTo('#commentlist').fadeIn(1000);
                                        $('#comment_count,.comment_count_int').text(parseInt($('#comment_count').text())+1);
                                        $('#comment').val('');
                                        fixup_corners();
                                    });
                            //} catch (e) {
                            //    console.log(e);
                            //    if (e instanceof RemoteException) {
                            //        console.log(e.toString());
                            //    }
                            //}
                            $('#comment_form :input').attr('disabled', false);

                            return false;
                        }
                    </script>
					<div id="respond" class="clearfix">
						<h2>{{i18n[lang]['post']['postyourcomment']}}</h2>

						<div class="cancel-comment-reply">
							<small><a rel="nofollow" id="cancel-comment-reply-link" href=
							"/view/post/{{post.id}}#respond" class="c3" name="cancel-comment-reply-link">{{i18n[lang]['post']['cancelreply']}}</a></small>
						</div>

						<form action="/post/view/{{post.id}}/comment" id="comment_form" name="comment_form" onsubmit="return do_comment()" method="post" class="form clearfix">
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