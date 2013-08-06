%cinclude part_html_decl
<head>
%	cinclude head notitle=1
	<script type="text/javascript" src="{{static('/js/Markdown.Converter.js')}}"></script>
	<script type="text/javascript" src="{{static('/js/Markdown.Editor.js')}}"></script>
	<link rel="stylesheet" href="{{static('/css/editor.css')}}"></link>
	<title>{{i18n[lang]['pages']['post_' + mode]['title']}}</title>
</head>
%cinclude part_html_body notitle=True
				<h1>{{i18n[lang]['pages']['post_' + mode]['title']}}</h1>
%				cinclude post_edit
%				cinclude comments
			</div>
%cinclude part_html_sidebar
	<script type="text/javascript">
		(function () {
			var converter = new Markdown.Converter();
			var editors = [];
			var langs = {{!str(i18n.keys())}};
			for (var i in langs) {
				var e = new Markdown.Editor(converter, "-" + langs[i]);
				editors.push(e);
				e.run();
			}
		})();
	</script>
</body>
</html>
