import os
import pkg_resources
from bottle import route, static_file as send_file
css_root 		= pkg_resources.resource_filename('hvsi', 'css')
css_image_root 	= pkg_resources.resource_filename('hvsi', 'images')
img_root 		= pkg_resources.resource_filename('hvsi', 'img')
js_root  		= pkg_resources.resource_filename('hvsi', 'js')
pdf_root 		= pkg_resources.resource_filename('hvsi', 'pdf')
wmd_root 		= pkg_resources.resource_filename('hvsi', 'wmd')
@route('/css/:file#.*#')
def static_css(file):
	return send_file(file, root=css_root)
@route('/css/images/:file#.*#')
def static_css_image(file):
	return send_file(file, root=css_image_root)
@route('/img/:file#.*#')
def static_img(file):
	return send_file(file, root=img_root)
@route('/wmd/images/:file')
def static_wmd_img(file):
	return send_file(file, root=img_root)
@route('/images/:file#.*#')
def static_img_2(file):
	return send_file(file, root=img_root)
@route('/js/:file#.*#')
def static_js(file):
	return send_file(file, root=js_root)
@route('/wmd/:file')
def static_wmd(file):
	return send_file(file, root=wmd_root)
@route('/pdf/:file')
def static_pdf(file):
	return send_file(file, root=pdf_root)

