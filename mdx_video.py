import markdown, re
NOBRACKET = r'[^}{]*'
BRK = ( r'{('
        + (NOBRACKET + r'({')*6
        + (NOBRACKET+ r'})*')*6
        + NOBRACKET + r')}' )
NOIMG = r'(?<!\!)'
LINK_RE = NOIMG + BRK + \
		  r'''\(\s*(<.*?>|((?:(?:\(.*?\))|[^\(\)]))*?)\s*((['"])(.*?)\12)?\)'''
class HTML5VideoExtension(markdown.Extension):
	def __init__(self, *args, **kwargs):
		markdown.Extension.__init__(self, *args, **kwargs)
	def extendMarkdown(self, md, md_globals):
		md.inlinePatterns.add('html5video', HTML5Video(LINK_RE), "<reference")
class HTML5Video(markdown.inlinepatterns.Pattern):
	def handleMatch(self, m):
		m = m.groups()
		name = m[1]
		src = [x for x in m[3:] if x][0]
		vid = markdown.etree.Element('video')
		vid.set('controls','controls')
		if 'youtube' not in src:
			src1 = markdown.etree.Element('source')
			src1.set('src',src + '.mp4')
			src1.set('type','video/mp4')
			src2 = markdown.etree.Element('source')
			src2.set('src',src + '.ogg')
			src2.set('type','video/ogg')
			vid.append(src1)
			vid.append(src2)
#			obj = markdown.etree.Element('object')
#			obj.set('type','application/x-shockwave-flash')
#			obj.set('data', "/flash/flvplayer.swf")
#			p1 = markdown.etree.Element('param')
#			p1.set('movie','/flash/flvplayer.swf')
#			p2 = markdown.etree.Element('param')
#			p2.set('name','flashvars')
#			p2.set('value','controlbar=over&file=' + src + '.m4v')
#			obj.append(p1)
#			obj.append(p2)
#			vid.append(obj)
		else:
			src1 = markdown.etree.Element('source')
			src1.set('src',src)
			vid.append(src1)
#		div = markdown.etree.Element('div')
#		div.set("class","fallback-text")
		return vid
		
def makeExtension(configs=None):
	return HTML5VideoExtension(configs=configs)