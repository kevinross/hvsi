# coding=utf-8
import copy
from i18n_e import i18n as e
from i18n_f import i18n as f
i18n_global = {
	'e': e,
	'f': f
}
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
