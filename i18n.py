# coding=utf-8
import copy, fnmatch, os, configobj
import pkg_resources
i18n_global = {}
try:
	files = pkg_resources.resource_listdir(__name__,'')
except:
	files = os.listdir('.') + os.listdir('./hvsi')
for file in fnmatch.filter(files, "i18n_*.ini"):
	if 'diff' in file:
		continue
	data = pkg_resources.resource_stream(__name__, file)
	c = configobj.ConfigObj(data, interpolation=False, indent_type='\t', encoding='utf-8', default_encoding='utf-8')
	lang = file.replace('i18n_','').replace('.ini','')
	i18n_global[lang] = c
def update_dict(orig, new):
	for k in new:
		if isinstance(new[k], dict):
			if k not in orig:
				orig[k] = new[k]
			else:
				update_dict(orig[k], new[k])
		else:
			orig[k] = new[k]
class i18n_over():
	def __init__(self, over=None):
		self.o = True if over else False
		if over:
			self.i18n = copy.deepcopy(i18n_global)
			update_dict(self.i18n, over)
	def __getitem__(self, i):
		if self.o:
			return self.i18n[i]
		else:
			return i18n_global[i]
	def __iter__(self):
		if self.o:
			return self.i18n.__iter__()
		else:
			return i18n_global.__iter__()
	def keys(self):
		if self.o:
			return self.i18n.keys()
		else:
			return i18n_global.keys()
def override_title(page, en, fr):
	return i18n_over(
		{
			'e': {
				'pages': {
					page: {
						'title': en
					}
				}
			},
			'f': {
				'pages': {
					page: {
						'title': fr
					}
				}
			}
		})
i18n = i18n_over()
