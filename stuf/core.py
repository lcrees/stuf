# -*- coding: utf-8 -*-
'''core stuf.'''

from itertools import chain
from operator import methodcaller, attrgetter
from collections import Mapping, MutableMapping, defaultdict, namedtuple

from stuf import exhaustitems
from stuf.iterable import exhaust
from stuf.desc import lazy_class, lazy
from stuf.deep import clsname, getcls, clsdict
from stuf.collects import OrderedDict, recursive_repr
from stuf.base import issequence, ismapping, maporseq
from stuf.six import map, getvalues, getitems, getkeys, isstring

__all__ = 'defaultstuf fixedstuf frozenstuf orderedstuf stuf'.split()

wraps = attrgetter('_wrapped')
delitem = attrgetter('_wrapped.__delitem__')
getitem = attrgetter('_wrapped.__getitem__')
setitem = attrgetter('_wrapped.__setitem__')
length = attrgetter('_wrapped.__len__')
_iter = attrgetter('_wrapped.__iter__')
asdict = attrgetter('_wrapped._asdict')


class corestuf(object):

    _map = dict
    _reserved = 'allowed _wrapped _map'.split()

    def __getattr__(self, key, _getter=object.__getattribute__):
        if key == 'iteritems':
            return getitems(self)
        elif key == 'iterkeys':
            return getkeys(self)
        elif key == 'itervalues':
            return getvalues(self)
        try:
            return self[key]
        except KeyError:
            return _getter(self, key)

    @recursive_repr()
    def __repr__(self):
        return '{0}({1})'.format(clsname(self), methodcaller('items')(self))

    @lazy_class
    def _classkeys(self):
        # protected keywords
        return frozenset(chain(
            iter(vars(self)), iter(vars(getcls(self))), self._reserved,
        ))

    @classmethod
    def _build(cls, iterable):
        # add class to handle potential nested objects of the same class
        kw = cls._map()
        if ismapping(iterable):
            kw.update(iterable)
        elif issequence(iterable):
            # extract appropriate key-values from sequence
            exhaust(map(kw.update, iterable))
        return kw

    @classmethod
    def _mapping(cls, iterable):
        return cls._map(iterable)

    @classmethod
    def _new(cls, iterable):
        return cls(cls._build(iterable))

    def _prepop(self, *args, **kw):
        kw.update(self._build(args))
        return kw

    @classmethod
    def _pop(cls, past, future):
        def closure(key, value, new=cls._new):
            if maporseq(value) and not isstring(value):
                # see if stuf can be converted to nested stuf
                trial = new(value)
                future[key] = trial if trial else value
            else:
                future[key] = value
        exhaustitems(closure, past)
        return cls._postpop(future)

    @classmethod
    def _postpop(cls, future):
        return future

    def copy(self):
        return self._new(self._map(self))


class writestuf(corestuf):

    def __setattr__(self, key, value):
        # handle normal object attributes
        if key == '_classkeys' or key in self._classkeys:
            clsdict(self)[key] = value
        # handle special attributes
        else:
            try:
                self[key] = value
            except KeyError:
                raise AttributeError(key)

    def __delattr__(self, key):
        # allow deletion of key-value pairs only
        if not key == '_classkeys' or key in self._classkeys:
            try:
                del self[key]
            except KeyError:
                raise AttributeError(key)

    def update(self, *args, **kw):
        self._pop(self._prepop(*args, **kw), self)


class wrapstuf(corestuf):

    def __init__(self, *args, **kw):
        super(wrapstuf, self).__init__()
        self._wrapped = self._pop(self._prepop(*args, **kw), self._map())

    @classmethod
    def _postpop(cls, future):
        return cls._mapping(future)


class writewrapstuf(wrapstuf, writestuf, MutableMapping):

    @lazy
    def __getitem__(self):
        return getitem(self)

    @lazy
    def __setitem__(self):
        return setitem(self)

    @lazy
    def __delitem__(self):
        return delitem(self)

    @lazy
    def __iter__(self):
        return _iter(self)

    @lazy
    def __len__(self):
        return length(self)

    def __reduce__(self):
        return (getcls(self), (wraps(self).copy(),))


class defaultstuf(writestuf, defaultdict):

    '''
    Dictionary with attribute-style access and a factory function to provide a
    default value for keys with no value.
    '''

    __slots__ = []

    _map = defaultdict

    def __init__(self, default, *args, **kw):
        '''
        :argument default: function that can provide default values
        :param *args: iterable of keys/value pairs
        :param **kw: keyword arguments
        '''
        defaultdict.__init__(self, default)
        writestuf.update(self, *args, **kw)

    @classmethod
    def _build(cls, default, iterable):
        kind = cls._map
        # add class to handle potential nested objects of the same class
        kw = kind(default)
        update = kw.update
        if ismapping(iterable):
            update(kind(default, iterable))
        elif issequence(iterable):
            # extract appropriate key-values from sequence
            def closure(arg):
                try:
                    update(arg)
                except (ValueError, TypeError):
                    pass
            exhaust(map(closure, iterable))
        return kw

    @classmethod
    def _new(cls, default, iterable):
        return cls(default, cls._build(default, iterable))

    def _prepop(self, *args, **kw):
        kw.update(self._build(self.default_factory, args))
        return kw

    def _pop(self, past, future):
        def closure(key, value, new=self._new, default=self.default_factory):
            if maporseq(value):
                # see if stuf can be converted to nested stuf
                trial = new(default, value)
                future[key] = trial if len(trial) > 0 else value
            else:
                future[key] = value
        exhaustitems(closure, past)

    def copy(self):
        return self._new(self.default_factory, dict(self))


class fixedstuf(writewrapstuf):

    '''
    Dictionary with attribute-style access where mutability is restricted to
    initial keys.
    '''

    def __setitem__(self, key, value):
        # only access initial keys
        if key in self.allowed:
            super(fixedstuf, self).__setitem__(key, value)
        else:
            raise KeyError('key "{0}" not allowed'.format(key))

    def _prepop(self, *args, **kw):
        iterable = super(fixedstuf, self)._prepop(*args, **kw)
        self.allowed = frozenset(iterable)
        return iterable

    def clear(self):
        wraps(self).clear()

    def popitem(self):
        raise AttributeError()

    def pop(self, key, default=None):
        raise AttributeError()


class frozenstuf(wrapstuf, Mapping):

    '''Immutable dictionary with attribute-style access.'''

    __slots__ = ['_wrapped']

    def __getitem__(self, key):
        try:
            return getattr(wraps(self), key)
        except AttributeError:
            raise KeyError('key {0} not found'.format(key))

    def __iter__(self):
        return iter(asdict(self)())

    def __len__(self):
        return len(asdict(self)())

    def __reduce__(self):
        return (getcls(self), (asdict(self)().copy(),))

    @classmethod
    def _mapping(self, mapping):
        return namedtuple('frozenstuf', iter(mapping))(**mapping)


class orderedstuf(writewrapstuf):

    '''Dictionary with dot attributes that remembers insertion order.'''

    _mapping = OrderedDict

    @lazy
    def __reversed__(self):
        return wraps(self).__reversed__


class stuf(writestuf, dict):

    '''Dictionary with attribute-style access.'''

    __slots__ = []
    __init__ = writestuf.update
