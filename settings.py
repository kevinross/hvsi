import os, sys
# SETTINGS could be a URL or the name of the module in the tree
# if it's a url]

try:
	base = os.path.dirname(os.environ['SETTINGS'])
	mod = os.path.basename(os.environ['SETTINGS']).replace('.py','')
	sys.path.append(base)
	instanceconfig = __import__(mod)
except:
	# last resort: use environment variables to configure the app.  Does not use defaults so
	# config_app will run if one of the required values isn't present
	from module_creator import importCode
	code = """
host		= %r
statichost	= %r
debug		= %r
timezone	= %r
dbprot		= %r
dbhost		= %r
dbport		= %r
dbuser		= %r
dbpass		= %r
dbdb		= %r
	""" % (
		os.environ['APP_HOST'],
		os.environ['APP_STATICHOST'],
		True if os.environ['APP_DEBUG'] == 'True' else False,
		os.environ['APP_TIMEZONE'],
		os.environ['APP_DBPROTO'],
		os.environ['APP_DBHOST'],
		int(os.environ['APP_DBPORT']),
		os.environ['APP_DBUSER'],
		os.environ['APP_DBPASS'],
		os.environ['APP_DB']
	)
	instanceconfig = importCode(code, 'instanceconfig')
