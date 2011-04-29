'''appspace utilities'''

from functools import wraps
from collections import OrderedDict

def lru_cache(maxsize=100):
    '''Least-recently-used cache decorator.

    From Raymond Hettinger

    Arguments to the cached function must be hashable.

    @param maxsize: maximum number of results in LRU cache
    '''
    def wrapped(func):
        # order: least recent to most recent
        cache = OrderedDict()
        @wraps(func)
        def wrapper(*args, **kw):
            key = args
            if kw: key += tuple(sorted(kw.items()))
            try:
                result = cache.pop(key)
            except KeyError:
                result = func(*args, **kw)
                # purge least recently used cache entry
                if len(cache) >= maxsize: cache.popitem(0)
            # record recent use of this key
            cache[key] = result
            return result
        return wrapper
    return wrapped


class lazy(object):

    '''Lazily assign attributes on an instance upon first use.'''

    def __init__(self, method):
        self.method = method
        try:
            self.__doc__ = method.__doc__
            self.__module__ = method.__module__
            self.__name__ = method.__name__
        except:
            pass

    def __get__(self, instance, cls=None):
        if instance is None: return self
        value = self.method(instance)
        setattr(instance, self.method.__name__, value)
        return value


class _commonstuff(dict):

    def __new__(cls, *arg, **kw):
        if isinstance(arg[0], dict):
            kw.update(arg[0])
            return cls((k, cls.__new__(v)) for k, v in kw.iteritems())
        elif isinstance(arg, (list, tuple)):
            return type(arg)(cls.__new__(v) for v in arg)
        raise TypeError('Invalid type for stuff')

    def __contains__(self, k):
        try:
            return hasattr(self, k) or super(_commonstuff, self).__contains__(k)
        except:
            return False

    def __iter__(self):
        return tuple(
            (k, tuple(v.__iter__())) for k, v in self.iteritems()
        )

    def __repr__(self):
        args = ', '.join(
            list('%s=%r' % (key, self[key]) for key in sorted(self.iterkeys()))
        )
        return '%s(%s)' % (self.__class__.__name__, args)

    def __setattr__(self, k, v):
        try:
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                self[k] = v
            except:
                raise AttributeError(k)
        else:
            object.__setattr__(self, k, v)


class frozenstuff(_commonstuff):

    def __new__(cls, *arg, **kw):
        if isinstance(arg[0], dict): kw.update(arg)
        slotter = dict(('__slots__', kw.keys()+cls.__dict__.keys()+['_store']))
        return type('frozenstuff', (super(frozenstuff, cls),), slotter)(kw)

    def __init__(self, kw):
        self._store = kw

    @lru_cache()
    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            try:
                value = self._store[k]
                self[k] = value
                object.__setattr__(self, k, value)
                return value
            except KeyError:
                raise AttributeError(k)

    @lru_cache
    def __getitem__(self, k):
        return super(frozenstuff, self).__getitem__(k)

    def __delattr__(self, k, w):
        raise AttributeError('__delattr__')

    def __delitem__(self, k, w):
        raise AttributeError('__delitem__')


class stuff(_commonstuff):

    '''A bunch of stuff.'''

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)

    def __delattr__(self, k):
        try:
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)
        else:
            object.__delattr__(self, k)