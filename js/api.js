var RemoteException = Class.create({
    initialize: function(exc, message) {
        this.exc = exc;
        this.message = message;
    },
    toString: function() {
        return this.exc + ': ' + this.message;
    }
});
function isString(o) {
    return o != null && (typeof o == "string" || (typeof o == "object" && o.constructor === String));
}
var base_endpoint = "/api";
var global_api = null;
var object_cache = {};
function __parse_response__(data) {
    return JSON.parse(data,  function(key, val) {
        if (isString(val) && val.indexOf("hash:")==0) {
            return jsonrpc("/api/" + val.replace("hash:", ""));
        }
        if (key=='sqlref') {
            this.objects = function(){return global_api.api.resolve_sqlobjs(val.name, val.items);};
            if (val.items.length == 1) {
                this.object = function(){return global_api.api.resolve_sqlobjs(val.name, val.items)[0];};
            }
            return;
        }
        var iso = /(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+)|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d)|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d)/;
        if (iso.match(val)) {
            return new Date(val);
        }
        return val;
    });
}
function __marshall_args__(oargs) {
    var args = oargs;
    for (var i=0;i<args.length;i++) {
        if (args[i] instanceof Object && '__meta__' in args[i]) {
            args[i] = {
                    one: true,
                    sqlref: {
                        name: args[i].__meta__.name,
                        items: [args[i].__meta__.id]
                    }
            };
        }
    }
    return args;
}
function __async_rpccall__(url, func) {
    var args = __marshall_args__(Array.prototype.slice.call(arguments, 2));
    var cb = args.pop();
    var params = {
        func: func,
        args: args
    }
    new Ajax.Request(url, {
        asynchronous: true,
        contentType: 'application/json',
        method: 'post',
        parameters: Object.toJSON(params),
        evalJS: 'force',
        requestHeaders: ['Cookie', document.cookie],
        onSuccess: function(response) {
            var data = __parse_response__(response.responseText);
            if (data.result == 1) {
                throw new RemoteException(data.exception, data.message);
            }
            if (cb != null) {
                cb(data.value);
            }
        }
    });
}
function __rpccall__(url, func) {
    var args = __marshall_args__(Array.prototype.slice.call(arguments, 2));
    var params = {
        func: func,
        args: args
    }
    var response = __parse_response__(new Ajax.Request(url, {
        asynchronous: false,
        contentType: 'application/json',
        method: 'post',
        parameters: Object.toJSON(params),
        evalJS: 'force',
        requestHeaders: ['Cookie', document.cookie]
    }).transport.responseText);
    if (response.result == 1) {
        throw new RemoteException(response.exception, response.message);
    }
    return response.value;
}
var JSONRPCBASE = Class.create({
        initialize: function(endpoint) {
            this.__endpoint__ = endpoint;
            this.__interface__ = __rpccall__(endpoint, "__interface__");
            this.__hash__ = this.__interface__.hash;
            this.__class__ = this.__interface__.name;
        },
        toString: function() {
            return '<' + this.__class__ + '@' + this.__hash__ + ' __endpoint__="' + this.__endpoint__+'">';
        },
        toJSON: function() {
            return 'hash:' + this.__hash__;
        }
    })
function jsonrpc(endpoint) {
    var API = Class.create(JSONRPCBASE);
    var result = new API(endpoint);
    var obj = {};
    for (var i=0; i<result.__interface__.funcs.length; i++) {
        obj[result.__interface__.funcs[i]] = __rpccall__.curry(result.__endpoint__, result.__interface__.funcs[i]);
        obj[result.__interface__.funcs[i]].async = __async_rpccall__.curry(result.__endpoint__, result.__interface__.funcs[i]);
    }
    API.addMethods(obj);
    for (var i=0; i<result.__interface__.attrs.length; i++) {
        (function(){
            var attr = result.__interface__.attrs[i];
            Object.defineProperty(result, attr, {
                get: function() {
                    // cache RPC objects only
                    var cache_key = result.__hash__ + '_' + attr;
                    if (cache_key in object_cache) {
                        return object_cache[cache_key];
                    }
                    var val = __rpccall__(base_endpoint, "globals.getattr", result, attr);
                    if (val instanceof Object && '__interface__' in val) {
                        object_cache[cache_key] = val;
                    }
                    return val;
                },
                set: function(value) {
                    __rpccall__(base_endpoint, "globals.setattr", result, attr, value);
                },
                configurable: true,
                enumerable: true
            });
        })();
    }
    return result;
}
global_api = null;
api = null;
globals = null;
function GLOBAL_API() {
    global_api = global_api || jsonrpc("/api");
    return global_api;
}
function API() {
    api = api || GLOBAL_API().api;
    return api;
}
function GLOBALS() {
    globals = globals || GLOBAL_API().globals;
    return globals;
}