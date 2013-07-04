import bottle, simplejson, requests, functools, re, datetime
from bottle import route, request, SimpleTemplate
bottle.debug(True)

date_re = r"(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+)|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d)|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d)"

def json(obj):
	if 'dict' in dir(obj):
		return obj.dict
	if '__rhash__' in dir(obj):
		return obj.__rhash__
	if isinstance(obj, list):
		return [json(x) for x in obj]
	if isinstance(obj, dict):
		return {x:json(obj[x]) for x in obj}
	if isinstance(obj, datetime.datetime):
		return obj.isoformat()
	return obj

def unjson(obj):
	if isinstance(obj, list):
		return [unjson(x) for x in obj]
	if isinstance(obj, dict):
		return {x:unjson(obj[x]) for x in obj}
	if isinstance(obj, basestring) and obj.startswith('hash:'):
		global objects
		return objects[int(obj.strip('hash:'))]
	return obj

def interface(obj):
	if hasattr(obj, '__interface__'):
		return obj.__interface__()
	return None

def resolve(obj, path):
	res = obj
	path = str(path)
	for comp in path.split('.'):
		res = getattr(res, comp)
	return res

objects = {}
def getobjects():
	global objects
	return objects.keys()

class JSONRPC(object):
	def __init__(self, *args, **kwargs):
		global objects
		objects[hash(self)] = self
	@property
	def dict(self):
		return ':'.join(['hash', str(hash(self))])
	def __interface__(self):
		return dict(
			name = self.__class__.__name__,
			hash = hash(self),
			attrs = [x for x in dir(self) if not callable(getattr(self, x)) and x not in ('__interface__', '__jsoncall__')],
			funcs = [x for x in dir(self) if callable(getattr(self, x)) and x not in ('__interface__', '__jsoncall__', '__class__')]
		)
	def __jsoncall__(self, sess=lambda:None):
		args = unjson(request.json.get('args', []))
		try:
			return dict(
				result=0,
				value=json(resolve(self, request.json['func'])(*args)))
		except Exception, e:
			from traceback import print_exc
			print_exc(e)
			return dict(
				result=1,
				exception=e.__class__.__name__,
				message=e.message
			)
	__getattr__ = object.__getattribute__
	__setattr__ = object.__setattr__

class Globals(JSONRPC):
	@staticmethod
	def allobjects():
		return getobjects()
	@staticmethod
	def getobject(key):
		global objects
		return objects[key]
	@staticmethod
	def echo(val):
		return val
	@staticmethod
	def getattr(obj, attr):
		return json(resolve(obj, attr))
	@staticmethod
	def setattr(obj, attr, val):
		if '.' not in attr:
			setattr(obj, attr, val)
			return
		obj = resolve(obj, '.'.join(attr.split('.')[0:-1]))
		setattr(obj, attr.split('.')[-1], val)
	# don't want people (re-)defining things here
	def __setattr__(self, key, value):
		raise AttributeError("can't set attribute")
class APIObj(JSONRPC):
	pass
class API(JSONRPC):
	def __init__(self, api):
		super(API, self).__init__()
		object.__setattr__(self, "globals", Globals())
		object.__setattr__(self, "api", api)
	# so I can reference objects by hash if needed
	def __getattr__(self, item):
		global objects
		try:
			item = int(item)
		except:
			pass
		if item in objects.keys():
			return objects[item]
		return object.__getattribute__(self, item)
	# don't want people (re-)defining things here
	def __setattr__(self, key, value):
		raise AttributeError("can't set attribute")

class RemoteException(Exception):
	def __init__(self, exc, msg):
		self.exc = exc
		self.msg = msg
	def __str__(self):
		return '%s: %s' % (self.exc, self.msg)
def datetime_decoder(d):
    if isinstance(d, list):
        pairs = enumerate(d)
    elif isinstance(d, dict):
        pairs = d.items()
    result = []
    for k,v in pairs:
        if isinstance(v, basestring):
            try:
                # The %f format code is only supported in Python >= 2.6.
                # For Python <= 2.5 strip off microseconds
                # v = datetime.datetime.strptime(v.rsplit('.', 1)[0],
                #     '%Y-%m-%dT%H:%M:%S')
                v = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                try:
                    v = datetime.datetime.strptime(v, '%Y-%m-%d').date()
                except ValueError:
                    pass
        elif isinstance(v, (dict, list)):
            v = datetime_decoder(v)
        result.append((k, v))
    if isinstance(d, list):
        return [x[1] for x in result]
    elif isinstance(d, dict):
        return dict(result)
resultcache = dict()
class Client(object):
	def __marshall_args__(self, args):
		return args
	def __parse_response__(self, ret):
		val = simplejson.loads(ret, object_hook=datetime_decoder)
		if val['result'] == 1:
			raise RemoteException(val['exception'], val['message'])
		if isinstance(val['value'], basestring) and 'hash:' in val['value']:
			return self.__class__(self.__base_endpoint__, val['value'].replace('hash:',''), self.__session__)
		if hasattr(self, '__resolve_references__'):
			return self.__resolve_references__(val['value'])
		return val['value']
	def __rpccall__(self, endpoint, func, *args):
		d = dict(func=func, args=(self.__marshall_args__(list(args) or [])))
		heads = {'content-type': 'application/json'}
		return self.__parse_response__(self.__session__.post(endpoint, data=simplejson.dumps(d), headers=heads).text)
	def __init__(self, base_endpoint, this_endpoint='', session=None):
		self.__base_endpoint__ = base_endpoint
		self.__endpoint__ = '/'.join([base_endpoint, this_endpoint]).rstrip('/')
		self.__session__ = session or requests.session()
		self.__interface__ = self.__rpccall__(self.__endpoint__, '__interface__')
		self.__rhash__ = 'hash:%i' % self.__interface__['hash']
	def __getattr__(self, item):
		if item in ('__base_endpoint__', '__endpoint__', '__session__', '__interface__',
					'__rpccall__', '__parse_response__', '__marshall_args__', '__rhash__'):
			return object.__getattribute__(self, item)
		key = (self.__rhash__, item)
		if item not in self.__interface__['funcs'] and item not in self.__interface__['attrs']:
			raise AttributeError('no attribute named %s exists' % item)
		result = None
		if key not in resultcache:
			if item in self.__interface__['funcs']:
				resultcache[key] = functools.partial(self.__rpccall__, self.__endpoint__, item)
			if item in self.__interface__['attrs']:
				result = self.__rpccall__(self.__base_endpoint__, 'globals.getattr', self.__rhash__, item)
				# only store clients
				if isinstance(result, Client):
					resultcache[key] = result
		return resultcache.get(key, result)
	def __setattr__(self, item, value):
		if item in ('__base_endpoint__', '__endpoint__', '__session__', '__interface__',
					'__rpccall__', '__parse_response__', '__marshall_args__', '__rhash__'):
			return object.__setattr__(self, item, value)
		if item in self.__interface__['funcs']:
			raise ValueError('will not attempt to change functions')
		if item in self.__interface__['attrs']:
			self.__rpccall__(self.__base_endpoint__, 'globals.setattr', self, item, value)

	def __json__(self):
		return self.__rhash__

	def __dir__(self):
		return sorted(self.__interface__['funcs'] + self.__interface__['attrs'])

objcache = dict()

class SqlRef(dict):
	def __getitem__(self, item):
		i = dict.__getitem__(self, item)
		if isinstance(i, dict) and 'sqlref' in i:
			# return resolved values instead!
			key = (i['sqlref']['name'], tuple(i['sqlref']['items']))
			if key not in objcache:
				objcache[key] =	self.__resolver__.__rpccall__(self.__resolver__.__base_endpoint__,
																'api.database.get',
																i['sqlref']['name'],
																i['sqlref']['items'])
				if len(objcache[key]) == 1:
					objcache[key] = objcache[key][0]
			return objcache[key]
		return i
	def __getattr__(self, item):
		if item in self:
			return object.__getattribute__(self, '__getitem__')(item)
		return object.__getattribute__(self, item)
	def __raw__(self):
		return {x:dict.__getitem__(self, x) for x in self}

	def __str__(self):
		return dict.__str__(self.__raw__())

	def __repr__(self):
		return dict.__repr__(self.__raw__())

	def __dir__(self):
		return self.__raw__().keys()



class APIClient(Client):
	def __marshall_args__(self, args):
		ret = super(APIClient, self).__marshall_args__(args)
		for i in range(0, len(ret) - 1):
			if isinstance(ret[i], Client):
				ret[i] = json(ret[i])
			elif isinstance(ret[i], dict) and '__meta__' in ret[i]:
				ret[i] = {'one': True,
						  'sqlref': {'name': ret[i]['__meta__']['name'],
									 'items': ret[i]['__meta__']['id']}}
		return ret
	def __resolve_references__(self, ret):
		def parse_sqlref(obj):
			if isinstance(obj, dict):
				for k in obj:
					if isinstance(obj[k], dict) and 'sqlref' in obj[k]:
						s = SqlRef(obj)
						s.__resolver__ = self
						return s
			elif isinstance(obj, list):
				return [parse_sqlref(x) for x in obj]
			return obj
		return parse_sqlref(ret)

def build_routes(api, sess=lambda:None):
	api_obj = API(api)
	@bottle.get('/api')
	def api():
		return api_obj.__jsoncall__(sess)
	@bottle.get('/api/:objid')
	def api(objid):
		global objects
		return objects[int(objid)].__jsoncall__(sess)
	@bottle.post('/api')
	def api():
		return api_obj.__jsoncall__(sess)
	@bottle.post('/api/:objid')
	def api(objid):
		global objects
		return objects[int(objid)].__jsoncall__(sess)

if __name__ == '__main__':
	build_routes(APIObj())
	@route('/')
	def main():
		return SimpleTemplate(source='<html><head> <script src="//ajax.googleapis.com/ajax/libs/prototype/1.7.1.0/prototype.js"></script><script src="/js/api.js" type="text/javascript"></script></head></html>').render()
	@route('/js/api.js')
	def js():
		return bottle.static_file('api.js', root='js')

	bottle.run(bottle.default_app(), port=9055)