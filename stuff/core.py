'''stuff'''

from collections import defaultdict
try:
    from collections import OrderedDict
except ImportError:
    from stuff.compat import OrderedDict

from stuff.util import lru_cache, lazy


def switchdict(**kw):
    factory = kw.pop('factory', False)
    order = kw.pop('order', False)
    if factory:
        sdict = defaultdict(factory)
    elif order:
        sdict = OrderedDict
    else:
        sdict = dict
    return sdict


class stuffdict(object):

    def __new__(cls, *arg, **kw):
        obj = switchdict(**kw)
        if arg and isinstance(arg[0], dict):
            if len(arg) > 1: raise TypeError('Invalid number of arguments')
            kw.update(arg[0])
            return obj((k, v) for k, v in kw.iteritems())
        elif isinstance(arg, (list, tuple)):
            return obj((k, v) for k, v in arg)
        raise TypeError('Invalid type for stuff')


class _commonstuff(object):

    def __new__(cls, *arg, **kw):
        obj = switchdict(**kw)
        if isinstance(arg[0], dict):
            kw.update(arg[0])
            return obj((k, cls.__init__(v)) for k, v in kw.iteritems())
        elif isinstance(arg, (list, tuple)):
            return obj((k, cls.__init__(v)) for k, v in arg)
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
        slotter = dict(
            ('__slots__', kw.keys()+cls.__dict__.keys()+['_store', '_fetcher'])
        )
        return type('frozenstuff', (super(frozenstuff, cls),), slotter)(kw)

    def __init__(self, kw):
        self._store = kw

    @lru_cache()
    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            try:
                value = self[k]
                object.__setattr__(self, k, value)
                return value
            except KeyError:
                raise AttributeError(k)

    @lru_cache
    def __getitem__(self, k):
        try:
            return super(frozenstuff, self).__getitem__(k)
        except KeyError:
            value = self._fetcher[k]
            self[k] = value
            return value

    def __setattr__(self, k, w):
        raise AttributeError('__setattr__')

    def __delattr__(self, k):
        raise AttributeError('__delattr__')

    def __delitem__(self, k):
        raise AttributeError('__delitem__')

    @lazy
    def _fetcher(self):
        return self._store


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