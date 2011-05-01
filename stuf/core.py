'''stuf'''

from collections import defaultdict
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


class _metafrozenstuf(type):

    def __new__(cls, name, base, classdict):
        def __init__(self, **kw):
            for k, v in kw.iteritems(): setattr(self, k, v)
        def __getattr__(self, k):
            return object.__getattribute__(self, k)
        @lru_cache()
        def __getitem__(self, k):
            return self.__getattr__(k)
        def __setattr__(self, k, v):
            object.__setattr__(self, k, v)
        def __repr__(self):
            return '%s(%r)' % (
                self.__class__.__name__,
                ', '.join(list('%s=%r' % (k, getattr(self, k))
                    for k in self.__slots__
                ))
            )
        newdict = dict(
            (k, v) for k, v in locals().iteritems() if k.startswith('__')
        )
        newdict['__slots__'] = classdict.keys() + newdict.keys()
        obj = type.__new__(cls, name, base, newdict)
        return obj


class frozenstuf(object):

    def __new__(cls, *arg, **kw):
        if arg:
            if isinstance(arg[0], dict):
                if len(arg) > 1: raise TypeError('Invalid number of arguments')
                kw.update(dict(**arg))
            elif isinstance(arg, (list, tuple)):
                kw.update(**dict((k, v) for k, v in arg))
        clsdict = dict(
            (k, v) for k, v in cls.__dict__.iteritems()
            if not k.startswith('__')
        )
        kw.update(clsdict)
        obj = _metafrozenstuf(cls.__name__, (object, ), kw)
        return obj(**kw)


class stuf(_basestuf):

    '''A bunch of stuf'''

    def __new__(cls, *arg, **kw):
        obj = type(cls.__name__, (cls._switchdict(kw), cls), {})
        if arg:
            if isinstance(arg[0], dict):
                if len(arg) > 1: raise TypeError('Invalid number of arguments')
                kw.update(arg[0])
                return obj(**dict((k, v) for k, v in kw.iteritems()))
            elif isinstance(arg, (list, tuple)):
                return obj(**dict((k, v) for k, v in arg))
        else:
            return obj(**dict((k, v) for k, v in kw.iteritems()))
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

    def __contains__(self, k):
        try:
            return hasattr(self, k) or super(stuf, self).__contains__(k)
        except:
            return False

    def __iter__(self):
        for k, v in self.iteritems(): yield (k, tuple(v.__iter__()))

    def __repr__(self):
        args = ', '.join(
            list('%s=%r' % (k, self[k]) for k in sorted(self.iterkeys()))
        )
        return '%s(%s)' % (self.__class__.__name__, args)


class stufdict(_basestuf):

    def __new__(cls, *arg, **kw):
        obj = cls._switchdict(kw)
        if arg and isinstance(arg[0], dict):
            if len(arg) > 1: raise TypeError('Invalid number of arguments')
            kw.update(arg[0])
            return obj((k, v) for k, v in kw.iteritems())
        elif isinstance(arg, (list, tuple)):
            return obj((k, v) for k, v in arg)
        return obj((k, v) for k, v in kw)