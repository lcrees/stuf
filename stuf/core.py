'''stuf'''

from collections import defaultdict
from _pyio import __metaclass__
try:
    from collections import OrderedDict
except ImportError:
    from stuff.compat import OrderedDict

from stuf.util import lru_cache, lazy


class _basestuf(object):

    @staticmethod
    def _switchdict(kw):
        factory = kw.pop('factory', False)
        order = kw.pop('order', False)
        if factory:
            sdict = defaultdict(factory)
        elif order:
            sdict = OrderedDict
        else:
            sdict = dict
        return sdict


class _commonstuf(_basestuf):

    def __contains__(self, k):
        try:
            return hasattr(self, k) or super(_commonstuf, self).__contains__(k)
        except:
            return False

    def __iter__(self):
        for k, v in self.iteritems(): yield (k, tuple(v.__iter__()))

    def __repr__(self):
        args = ', '.join(
            list('%s=%r' % (k, self[k]) for k in sorted(self.iterkeys()))
        )
        return '%s(%s)' % (self.__class__.__name__, args)



class frozenstuf(object):

    def __new__(cls, *arg, **kw):
        base = _basestuf._switchdict(kw)
        oldkw = kw = base(**kw.copy())
        if arg:
            if isinstance(arg[0], dict):
                if len(arg) > 1: raise TypeError('Invalid number of arguments')
                kw.update(**arg)
                oldkw.update(base(**arg))
            elif isinstance(arg, (list, tuple)):
                kw.update(**dict((k, v) for k, v in arg))
                oldkw.update(**base((k, v) for k, v in arg))
        kw['__slots__'] = kw.keys() + ['_store']
        newcls = type(cls.__name__, (cls,), kw)
        return newcls(oldkw)

    @lazy
    def _fetcher(self):
        return self.__class__(self._store)

    def __init__(self, kw):
        self._store = kw

    def __getattr__(self, k):
        try:
            value = self[k]
            object.__setattr__(self, k, value)
            return value
        except KeyError:
            raise AttributeError(k)

    @lru_cache
    def __getitem__(self, k):
        return self._fetcher[k]

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False
        return True

    def __cmp__(self, other):
        if other is None: return False
        if isinstance(other, frozenstuf):
            return self._fetcher, dict(other.iteritems())

    def __iter__(self):
        for k in self._fetcher.iterkeys(): yield k

    def __len__(self):
        return len(self._fetcher.keys())

    def __repr__(self):
        args = ', '.join(
            list('%s=%r' % (k, self[k]) for k in sorted(self.iterkeys()))
        )
        return '%s(%s)' % (self.__class__.__name__, args)

    def get(self, key, default=None):
        '''Fetch a given key from the mapping. If the key does not exist,
        return the default.

        @param key Keyword of item in mapping.
        @param default Default value (default: None)
        '''
        try:
            return self[key]
        except KeyError:
            return default

    def items(self):
        '''Returns a list with all key/value pairs in the store.'''
        return list(self.iteritems())

    def iteritems(self):
        '''Lazily returns all key/value pairs in a store.'''
        for k in self: yield (k, self[k])

    def itervalues(self):
        '''Lazily returns all values in a store.'''
        for _, v in self.iteritems(): yield v

    def keys(self):
        '''Returns a list with all keys in a store.'''
        return list(self.iterkeys())

    def values(self):
        '''Returns a list with all values in a store.'''
        return list(self.itervalues())


class stuf(_commonstuf):

    '''A bunch of stuf'''

    def __new__(cls, *arg, **kw):
        obj = type(cls.__name__, (cls._switchdict(kw), cls), {})
        if arg:
            if isinstance(arg[0], dict):
                if len(arg) > 1: raise TypeError('Invalid number of arguments')
                kw.update(arg[0])
                return type(cls.__name__, (obj, cls), {})(
                    **dict((k, cls.__init__(v)) for k, v in kw.iteritems()
                ))
            elif isinstance(arg, (list, tuple)):
                return type(cls.__name__, (obj, cls), {})(
                    **dict((k, cls.__init__(v)) for k, v in arg)
                )
        else:
            return type(cls.__name__, (obj, cls), {})(
                **dict((k, cls.__init__(v)) for k, v in kw.iteritems())
            )
        raise TypeError('Invalid type for stuf')

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)

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


class stufdict(_basestuf):

    def __new__(cls, *arg, **kw):
        obj = cls._switchdict(kw)
        if arg and isinstance(arg[0], dict):
            if len(arg) > 1: raise TypeError('Invalid number of arguments')
            kw.update(arg[0])
            return obj((k, v) for k, v in kw.iteritems())
        elif isinstance(arg, (list, tuple)):
            return obj((k, v) for k, v in arg)
        raise TypeError('Invalid type for stuf')