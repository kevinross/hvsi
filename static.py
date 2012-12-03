import os, copy
import pkg_resources, mimetypes
from bottle import route, request, HTTPResponse
for i in ('css', 'css/images', 'img', 'wmd/images','images','js','wmd','pdf'):
	path = '/%s/:file' % i
	@route(path)
	def static_file(file, i=i):
		mimetype, encoding = mimetypes.guess_type(file)
		headers = dict()
		if mimetype: headers['Content-Type'] = mimetype
		if encoding: headers['Content-Encoding'] = encoding
		return HTTPResponse(pkg_resources.resource_stream('hvsi', '%s/%s' % (i, file)), **headers)

