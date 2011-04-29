'''stuff'''

from collections import defaultdict
try:
    from collections import OrderedDict
except ImportError:
    from stuff.compat import OrderedDict

from stuff.util import lru_cache


class switchdict(dict):

    def __new__(cls, **kw):
        factory = kw.pop('factory', False)
        if factory: return defaultdict(factory)
        order = kw.pop('order', False)
        if order: return OrderedDict
        return dict


class stuffdict(switchdict):

    def __new__(cls, *arg, **kw):
        if isinstance(arg[0], dict):
            if len(arg) > 1: raise TypeError('Invalid number of arguments')
            kw.update(arg[0])
            return super(cls, stuffdict).__new__(**kw).__init__(
                (k, v) for k, v in kw.iteritems()
            )
        elif isinstance(arg, (list, tuple)):
            return super(cls, stuffdict).__new__(**kw).__init__(
                (k, v) for k, v in arg
            )
        raise TypeError('Invalid type for stuff')


class _commonstuff(switchdict):

    def __new__(cls, *arg, **kw):
        if isinstance(arg[0], dict):
            kw.update(arg[0])
            return super(cls, stuffdict).__new__(**kw).__init__(
                (k, cls.__init__(v)) for k, v in kw.iteritems()
            )
        elif isinstance(arg, (list, tuple)):
            return super(cls, stuffdict).__new__(**kw).__init__(
                (k, cls.__init__(v)) for k, v in arg
            )
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
            list('%s=%r' % (k, self[k]) for k in sorted(self.iterkeys()))
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