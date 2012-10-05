WSGIScriptAlias / /var/webapps/hvsi/app.wsgi

WSGIDaemonProcess hvsi.ca processes=4 threads=8
WSGIProcessGroup hvsi.ca

