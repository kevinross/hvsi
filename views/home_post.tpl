%			if 'post' in globals():
%import calendar
				<div class="post type-post hentry category-uncategorized">
					<div class="meta">
						{{post.time.day}} {{calendar.month_name[post.time.month]}} {{post.time.year}} //
%					if request.admin:
						<a class="post-edit-link" href="/post/edit/" title="{{i18n[lang]['post']['edit_post']}}">{{i18n[lang]['post']['edit_entry']}}</a>
%					end
					</div>
					<div class="comment_count">
						<a href="/post/#respond" title="Comment on A Regular Post">{{post.comments.count()}}</a>
					</div>

					<h1><a href="/post/" rel="bookmark" title="{{i18n[lang]['post']['permalink']}} {{getattr(post, 'title_' + lang)}}">{{getattr(post, 'title_' + lang)}}</a></h1>

					<div class="body">
						<p>{{getattr(post, 'html_' + lang)}}</p>
					</div>

				</div>
%			end
