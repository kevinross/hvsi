import os, sys, urlimport
# SETTINGS could be a URL or the name of the module in the tree
# if it's a url, urlimport will import it.  If not, standard machinery will import it
base = os.path.dirname(os.environ.get('SETTINGS', ''))
mod = os.path.basename(os.environ.get('SETTINGS', 'instanceconfig')).replace('.py','')
sys.path.append(base)
instanceconfig = __import__(mod)