%from imports import *
						<h2><a href="http://twitter.com/uoHvsI">Twitter</a></h2>
						<div id="tweet" />
						<script type="text/javascript">
							$("#tweet").tweet({
								avatar_size: 32,
								count: 5,
								fetch: 10,
								username: "uoHvsI",
								filter: function(t){ return ! /^@\w+/.test(t.tweet_raw_text); },
								template: '<a class="tweet_link" href="{tweet_url}" title="view tweet on twitter">{tweet_relative_time}</a>:&nbsp;{text}'
							});
						</script>
