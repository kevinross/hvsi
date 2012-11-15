				<div class="post mode-post hentry category-uncategorized">
%				if mode=="create":
					<form action="/post/create" method="post">
%				else:
					<form id='post_editor' action="/post/edit/{{post.id}}" method="post">
%				end
%				if request.session.data:
%					data = simplejson.loads(request.session.data)
%					request.session.data = None
%				else:
%					data = dict()
%				end
%					for i in i18n.keys():
						<div class="post_editor">
							<div>
								<label for="title_{{i}}">
									{{i18n[i]['pages'][page]['post_title']}} ({{i18n[i]['lang']}}):
								</label>
							</div>
							<div>
								<input mode="textbox" name="title_{{i}}" value="{{data.get('title_' + i, '') if mode=='create' else getattr(post,'title_' + i)}}"/>
							</div>
							<div>
								<label for="content_e">
									{{i18n[i]['pages'][page]['post_content']}} ({{i18n[i]['lang']}}):
								</label>
							</div>
							<div>
								<textarea rows=10 cols=70 id="content_{{i}}" name="content_{{i}}">{{data.get('content_' + i, '') if mode=='create' else getattr(post,'content_' + i)}}</textarea>
								<input type="hidden" id="content_{{i}}_hidden" name="content_{{i}}_hidden" value="{{data.get('content_' + i + '_hidden', '')}}" />
							</div>
							<br/>
							<br/>
							<div style="border:1px solid black; padding: 10px;" class="wmd-preview" id="preview_{{i}}">&nbsp;</div>
							<br/>
							<br/>
						</div>
%					end
						<div>
							<label for="allow_comments">
								{{i18n[lang]['pages'][page]['allow_comments']}}
							</label>
						</div>
						<div>
							<input type="checkbox" name="allow_comments" {{'' if mode=='create' else ('checked="1"' if post.allow_comments else '')}}/>
						</div>
						<div style="width: 100%; height: 100%;">
							<button style="float: none; width: 100px; margin: 10px auto;" value="{{i18n[lang]['pages']['create_editpost']['cancel']}}" onclick="history.back()">{{i18n[lang]['pages'][page]['cancel']}}</button>
							<input style="float: none; width: 100px; margin: 10px auto;" type="submit" value="{{i18n[lang]['pages']['post_' + mode]['submit']}}" />
						</div>
					</form>
				</div>