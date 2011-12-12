# -*- coding: utf-8 -*-
'''special stuf'''

from __future__ import absolute_import
from operator import eq
from itertools import imap
from functools import partial

from .core import stuf
from .util import OrderedDict, lazy, lazy_class


class defaultstuf(stuf):

    '''
    dictionary with dot attributes and a factory function that provides a 
    default value for keys with no value
    '''

    def __getstate__(self):
        return dict(
            content=dict(i for i in self),
            factory=self._factory,
            fargs=self._fargs,
            fkw=self._fkw,
        )

    def __setstate__(self, state):
        return self._d_fromiter(
            factory=state['factory'],
            fargs=state['fargs'],
            fkw=state['fkw'],
            src=state['content'],
        )

    def __missing__(self, k):
        # provides missing value if there's a factory function
        factory = self._factory
        if factory is not None:
            self[k] = factory(*self._fargs, **self._fkw)
            return self[k]
        return None

    ## pylint: disable-msg=e0202
    @classmethod
    def _fromiter(cls, factory=None, fargs=None, fkw=None, src=None, sq=None): 
        '''
        builds stuf from stuff with a factory function/arguments/keywords

        @param factory: factory function that returns default value
        @param fargs: positional arguments for factory function
        @param fkw: keyword arguments for factory function
        @param src: iterable of key-value pairs
        @param sq: list of sequence types
        '''
        if fargs is None:
            fargs = ()
        if fkw is None:
            fkw = {}
        if src is None:
            src = ()
        if sq is None:
            sq = [list, tuple]
        src = cls._build(src=src)
        src.update(fargs=fargs, factory=factory, fkw=fkw)
        return cls(src)
    ## pylint: enable-msg=e0202

    @classmethod
    def _fromkw(cls, factory=None, fargs=(), fkw=None, **kw):
        '''
        builds stuf from keywords with a factory function/arguments/keywords

        @param factory: factory function that returns default value
        @param fargs: positional arguments for factory function
        @param fkw: keyword arguments for factory function
        '''
        if fkw is None:
            fkw = {}
        return cls._d_fromiter(factory, fargs, fkw, kw)

    def _preprepare(self, arg):
        # preserve factory function, arguments, keywords
        factory = arg.pop('factory')
        fargs = arg.pop('fargs')
        fkw = arg.pop('fkw')
        self._factory = factory
        self._fargs = fargs
        self._fkw = fkw
        # rebuild fromiter as partial functions
        self._fromiter = partial(
            self._d_fromiter,
            factory=factory,
            fargs=fargs,
            fkw=fkw,
        )
        return arg

    def copy(self):
        # copy factory function, arguments, keywords
        return self._d_fromiter(
            factory=self._factory,
            fargs=self._fargs,
            fkw=self._fkw,
            src=dict(i for i in self),
        )


class orderedstuf(stuf):

    '''dictionary with dot attributes that remembers insertion order'''

    def __setitem__(self, k, v):
        if k not in self:
            root = self._root
            last = root[0]
            last[1] = root[0] = self._map[k] = [last, root, k]
        super(self.__class__, self).__setitem__(k, v)

    def __delitem__(self, k):
        super(orderedstuf, self).__delitem__(k)
        link = self._map.pop(k)
        link_prev = link[0]
        link_next = link[1]
        link_prev[1] = link_next
        link_next[0] = link_prev

    def __getstate__(self):
        return tuple(i for i in self)

    def __reduce__(self):
        return self.__class__, (tuple(i for i in self),)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return len(self)==len(other) and all(
                imap(eq, self.iteritems(), other.iteritems())
            )
        return super(self.__class__, self).__eq__(other)

    def __iter__(self):
        root = self._root
        curr = root[1]
        # return in order
        while curr is not root:
            key = curr[2]
            value = self[key]
            if isinstance(value, self.__class__):
                yield key, tuple(i for i in value)
            else:
                yield key, value
            curr = curr[1]

    def __reversed__(self):
        root = self._root
        curr = root[0]
        while curr is not root:
            yield curr[2]
            curr = curr[0]

    @lazy
    def _populate(self):
        # extend _BaseStuf._populate with default sequence
        return partial(self._b_saddle, sq=[tuple, dict, list])

    @lazy_class
    def _build(self):
        # extend _BaseStuf._build with default sequence and attache to class
        return partial(self._b_todict, type_=OrderedDict, maps=[dict])

    @lazy
    def _update(self):
        # extend _BaseStuf._update with default sequence
        return partial(self._b_update, seqs=(OrderedDict, tuple, dict, list))

    def _preprepare(self, arg):
        # prep for ordered sequence
        self._root = root = [None, None, None]
        root[0] = root[1] = root
        self._map = {}
        return arg

    def clear(self):
        try:
            # clear order info
            for node in self._map.itervalues(): del node[:]
            self._root[:] = [self._root, self._root, None]
            self._map.clear()
        except AttributeError:
            pass
        super(self.__class__, self).clear()

    def copy(self):
        return self._b_fromiter(list(i for i in self))

    def items(self):
        return list((k, v) for k, v in self.iteritems())

    def iteritems(self):
        for k in self: 
            yield k[0], self[k[0]]

    def iterkeys(self):
        for k in self: 
            yield k[0]

    def itervalues(self):
        for k in self: 
            yield self[k[0]]

    def keys(self):
        return list(i for i in self.iterkeys())

    def popitem(self, last=True):
        if not self: 
            raise KeyError('dictionary is empty')
        k = next(reversed(self) if last else iter(self))
        v = self.pop(k)
        return k, v

    def values(self):
        return list(i for i in self.itervalues())
