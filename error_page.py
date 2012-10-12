# coding=utf-8
from bottle import SimpleTemplate
ERROR_PAGE_TEMPLATE = SimpleTemplate(u"""
%try:
    %from bottle import DEBUG, HTTP_CODES, request
    %from i18n import i18n
    %if hasattr(request, 'logged_in') and request.logged_in:
    %	lang = request.user.language
    %elif 'lang' in request.cookies:
    %	lang = request.cookies['lang']
    %else:
    %	lang = 'e'
    %end
    %status_name = HTTP_CODES.get(e.status, 'Unknown').title()
    <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
    <html>
        <head>
            <title>{{i18n[lang]['pages']['http_error']['title']}} {{e.status}}: {{status_name}}</title>
            <style type="text/css">
              html {background-color: #eee; font-family: sans;}
              body {background-color: #fff; border: 1px solid #ddd; padding: 15px; margin: 15px;}
              pre {background-color: #eee; border: 1px solid #ddd; padding: 5px;}
            </style>
        </head>
        <body>
            <h1>{{i18n[lang]['pages']['http_error']['title']}} {{e.status}}: {{status_name}}</h1>
            <p>{{i18n[lang]['pages']['http_error']['sorry_part_1']}} <tt>{{request.url}}</tt> {{i18n[lang]['pages']['http_error']['sorry_part_2']}}:</p>
            <pre>{{str(e.output)}}</pre>
            <p><button onclick="history.back()">{{i18n[lang]['pages']['http_error']['back']}}</button></p>
            %if DEBUG and e.exception:
              <h2>Exception:</h2>
              <pre>{{repr(e.exception)}}</pre>
            %end
            %if DEBUG and e.traceback:
              <h2>Traceback:</h2>
              <pre>{{e.traceback}}</pre>
            %end
        </body>
    </html>
%except ImportError:
    <b>ImportError:</b> Could not generate the error page. Please add bottle to sys.path
%end
""")