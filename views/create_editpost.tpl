%if 'i18n' not in globals():
	%from i18n import i18n
%end
%import calendar
%cinclude parts part=1
<head>
%	cinclude head
</head>
%cinclude parts part=2
				<h1>{{i18n[lang]['pages'][page]['title']}}</h1>
%				cinclude post_edit template_settings=dict(noescape=True)
%				cinclude comments
			</div>
%cinclude parts part=3
	<script type="text/javascript">
        /***** Tell WMD not to start up automatically *****/
        // Set this *before* you load wmd.js
        // Otherwise you'll end up with two editors on top of each other!
        wmd_options = { autostart: false };
    </script>
	<script type="text/javascript" src="/wmd/wmd.js"></script>
	<script>
		instances = []
		function set_content() {
%	  for i in i18n:
			document.getElementById('content_{{i}}_hidden').value = document.getElementById('content_{{i}}').value;
%	  end
			setTimeout('set_content()',200);
		}
		setTimeout('set_content()',200);
		function createEditors() {
            if (!Attacklab || !Attacklab.wmd) {
                alert("WMD hasn't finished loading!");
                return;
            }
%		  for i in i18n:
            $('body').keyup(function() {
            	document.getElementById('content_{{i}}_hidden').value = document.getElementById('content_{{i}}').value;
            });
            var {{i}}_txt = document.getElementById('content_{{i}}');
            var {{i}}_div = document.getElementById('preview_{{i}}');
            var {{i}}_panes = {input:{{i}}_txt, preview:{{i}}_div, output:null};
            var {{i}}_previewManager = new Attacklab.wmd.previewManager({{i}}_panes);
            var {{i}}_editor = new Attacklab.wmd.editor({{i}}_txt,{{i}}_previewManager.refresh);
            instances.push({pm:{{i}}_previewManager,ed:{{i}}_editor});
%		  end
        }
        createEditors();
        $('#post_editor').submit(function() {
%		  for i in i18n:
			var e = instances.pop();
			e.pm.destroy();
			e.ed.destroy();
%		  end
        });
	</script>
</body>
</html>