'''stuf'''

from inspect import ismethod
try:
    from collections import OrderedDict
except ImportError:
    from stuf.compat import OrderedDict

from stuf.util import lru_cache


class stuf(dict):

    '''stuf'''

    def __init__(self, *args, **kw):
        self.update(*args, **kw)

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

    def __iter__(self):
        for k, v in self.iteritems(): yield (k, tuple(v.__iter__()))

    @staticmethod
    def _args2dict(*args, **kw):
        if args:
            if len(args) > 1:
                raise TypeError('Invalid number of arguments %s' % len(args))
            source = args[0]
            if isinstance(source, dict):
                kw.update(source)
            elif isinstance(source, (list, tuple)):
                for arg in source:
                    if isinstance(arg, (list, tuple)) and len(arg) == 2:
                        kw[arg[0]] = arg[-1]
        return kw

    def update(self, *args, **kw):
        cls = self.__class__
        for k, v in self._args2dict(*args, **kw).iteritems():
            if isinstance(v, (tuple, dict, list)):
                trial = cls(v)
                if len(trial) > 0:
                    self[k] = trial
                else:
                    self[k] = v
            else:
                self[k] = v


class defaultstuf(stuf):

    _factory = None
    _fargs = None

    def __init__(self, factory, *args, **kw):
        self._factory = factory
        if args:
            self._fargs = args[0]
        else:
            self._fargs = ()
        self.update(*args[1:], **kw)

    def __missing__(self, key):
        self[key] = self._factory(*self._fargs)
        return self[key]

    def update(self, *args, **kw):
        factory = self._factory
        fargs = self._fargs
        cls = self.__class__
        for k, v in self._args2dict(*args, **kw).iteritems():
            if isinstance(v, (tuple, dict, list)):
                trial = cls(factory, fargs, v)
                if len(trial) > 0:
                    self[k] = trial
                else:
                    self[k] = v
            else:
                self[k] = v


class orderedstuf(OrderedDict):

    def __init__(self, *args, **kw):
        super(orderedstuf, self).__init__(self)
        self.update(*args, **kw)

    def __getattr__(self, k):
        if k in self._methods:
            return object.__getattribute__(self, k)
        else:
            try:
                return self[k]
            except KeyError:
                raise AttributeError(k)

    def __setattr__(self, k, v):
        if k in self._methods:
            object.__setattr__(self, k, v)
        else:
            try:
                self[k] = v
            except:
                raise AttributeError(k)

    def __delattr__(self, k):
        if k in self._methods:
            object.__delattr__(self, k)
        else:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

    @staticmethod
    def _args2dict(*args, **kw):
        newdict = OrderedDict()
        if args:
            if len(args) > 1:
                raise TypeError('Invalid number of arguments %s' % len(args))
            source = args[0]
            if isinstance(source, (OrderedDict, dict)):
                newdict.update(source)
            elif isinstance(source, (list, tuple)):
                for arg in args:
                    if isinstance(arg, (list, tuple)) and len(arg) == 2:
                        newdict[arg[0]] = arg[-1]
        newdict.update(kw)
        return newdict

    @property
    def _methods(self):
        first = ['__map', '__root'] + list(
            k for k, v in self.__dict__.iteritems() if ismethod(v)
        )
        first += list('_OrderedDict'+k for k in first)
        return frozenset(first)

    def update(self, *args, **kw):
        cls = self.__class__
        for k, v in self._args2dict(*args, **kw).iteritems():
            if isinstance(v, (OrderedDict, tuple, dict, list)):
                trial = cls(v)
                if len(trial) > 0:
                    self[k] = trial
                else:
                    self[k] = v
            else:
                self[k] = v


class fixedstuf(object):

    '''fixed stuf'''

    _basekeys = None
    _keys = None
    _stuf = None

    def __init__(self, *args, **kw):
        kw = self._args2dict(*args, **kw)
        self._keys = frozenset(kw.keys())
        cls = self.__class__
        self._stuf = stuf = dict()
        self.update(**kw)

    @lru_cache()
    def __getitem__(self, k):
        if k in self._keys:
            return self._stuf[k]
        else:
            raise KeyError(k)

    def __setitem__(self, k, v):
        if k in self._keys:
            self._stuf[k] = v
        else:
            raise KeyError(k)

    def __delitem__(self, k):
        pass

    def __getattr__(self, k):
#        if k in self._methods:
        try:
            return object.__getattribute__(self, k)
        except AttributeError:
            if k in self._keys:
                try:
                    return self[k]
                except KeyError:
                    raise AttributeError(k)
            else:
                raise AttributeError(k)

    def __cmp__(self, *args):
        return self._stuf.__cmp__(*args)

    def __contains__(self, k):
        return self._stuf.__contains__(k)

    def __setattr__(self, k, v):
        if k in self._methods:
            object.__setattr__(self, k, v)
        elif k in self._keys:
            try:
                self[k] = v
            except:
                raise AttributeError(k)
        else:
            raise AttributeError(k)

    def __delattr__(self, *args, **kwargs):
        pass

    def __gt__(self, *args):
        return self._stuf.__gt__(*args)

    def __iter__(self):
        return self._stuf.__iter__()

    def __len__(self):
        return self._stuf.__len__()

    def __lt__(self, *args):
        return self._stuf.__lt__(*args)

    def __reduce__(self):
        return self._stuf.__reduce__()

    def __reduce_ex__(self):
        return self._stuf.__reduce_ex__()

    def __repr__(self):
        return self._stuf.__repr__()

    def __sizeof__(self):
        return self._stuf.__sizeof__()

    def __str__(self):
        return self._stuf.__str__()

    @staticmethod
    def _args2dict(*args, **kw):
        if args:
            if len(args) > 1:
                raise TypeError('Invalid number of arguments %s' % len(args))
            source = args[0]
            if isinstance(source, dict):
                kw.update(source)
            elif isinstance(source, (list, tuple)):
                for arg in source:
                    if isinstance(arg, (list, tuple)) and len(arg) == 2:
                        kw[arg[0]] = arg[-1]
        return kw

    @property
    def _methods(self):
#        if self._basekeys is not None: return self._basekeys
        return frozenset(list(
            k for k, v in self.__dict__.iteritems() if ismethod(v)
        ) + ['_keys', '_stuf'])
#        return self._basekeys

    def items(self):
        return self._stuf.items()

    def iteritems(self):
        return self._stuf.iteritems()

    def iterkeys(self):
        return self._stuf.iterkeys()

    def itervalues(self):
        return self._stuf.itervalues()

    def keys(self):
        return self._stuf.keys()

    def pop(self, k):
        pass

    def popitem(self, *args, **kwargs):
        pass

    def setdefault(self, k, default):
        return self._stuf.setdefault(k, default)

    def update(self, *args, **kw):
        cls = self.__class__
        stf = self._stuf
        for k, v in self._args2dict(*args, **kw).iteritems():
            if isinstance(v, (tuple, dict, list)):
                trial = cls(v)
                if len(trial) > 0:
                    stf[k] = trial
                else:
                    stf[k] = v
            else:
                stf[k] = v

    def values(self):
        return self._stuf.values()