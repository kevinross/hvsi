						<h2><a href="http://twitter.com/uoHvsI">Twitter</a></h2>
						<ul>
%						  for tweet in db.Twitter.latest[0:5]:
%						   twe = ''
%						   for c in tweet.text:
%							twe = twe + c + ('<wbr/>' if c == ' ' else '')
%						   end
							<li><span class="sidebar_key" style="text-align: left; padding: 2px; width: 100%;">{{twe}}</span></li>
%						  end
						</ul>
