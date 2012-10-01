def show_paths(cur, e, f):
	for k in e:
		if k in f:
			if isinstance(f[k], dict):
				show_paths(cur + '/' + k, e[k], f[k])
		else:
			if isinstance(e[k], dict):
				print "dict:", cur + '/' + k
			else:
				print cur + '/' + k
from i18n_e import i18n as e
from i18n_f import i18n as f

print "French missing:"
show_paths('',e,f)

print ""
print "English missing:"
show_paths('',f,e)
