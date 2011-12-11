# -*- coding: utf-8 -*-
'''restricted stuf'''

from __future__ import absolute_import

from operator import eq
from itertools import imap

from .base import basestuf
from .util import lazy, lru_wrapped


class restrictedstuf(basestuf):

    '''restricted stuf'''

    def __getitem__(self, key):
        if key in self._keys: 
            return self._stuf[key]
        raise KeyError(key)

    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            try:
                value = object.__getattribute__(self._stuf, key)
                object.__setattr__(self, key, value)
                return value
            except AttributeError:
                if key in self._keys: 
                    return self._stuf[key]
                raise AttributeError(key)

    def __delattr__(self, k):
        raise TypeError(u'"%s"s are immutable' % self.__class__.__name__)

    def __eq__(self, other):
        # compare to other stuf
        if isinstance(other, self.__class__):
            return len(self)==len(other) and all(
                imap(eq, iter(self), iter(other))
            )
        # compare to dict
        elif isinstance(other, dict):
            return len(self)==len(other) and all(
                imap(eq, self.iteritems(), other.iteritems())
            )
        return False

    @lazy
    def _stuf(self):
        # default internal dictionary
        return {}

    @lazy
    def _update(self):
        return self._b_update

    def _preprepare(self, arg):
        # preserve keys
        self._keys = frozenset(arg.iterkeys())
        return arg


class fixedstuf(restrictedstuf):

    '''dict with dot attributes and mutability restricted to initial keys'''

    def __setitem__(self, k, v):
        # only access initial keys
        if k in self._keys:
            self._stuf[k] = v
        else:
            raise KeyError(k)

    def __setattr__(self, k, v):
        # allow normal object creation for protected keywords
        if k == '_classkeys' or k in self._classkeys:
            object.__setattr__(self, k, v)
        elif k in self._keys:
            # look in stuf
            try:
                self._stuf[k] = v
            except:
                raise AttributeError(k)
        else:
            raise AttributeError(k)

    def __reduce__(self):
        return self.__class__, (dict(i for i in self),)

    @lazy
    def update(self):
        return self._c_update



class frozenstuf(restrictedstuf):

    '''Immutable dict with dot attributes'''

    def __setattr__(self, k, v):
        # allow object setting for existing class members
        if k == '_classkeys' or k in self._classkeys:
            object.__setattr__(self, k, v)
        else:
            raise TypeError(u'%s is immutable' % self.__class__.__name__)

    def __reduce__(self):
        return self.__class__, (dict(i for i in self),)

    @lazy
    def __getitem__(self):
        # cache it
        return lru_wrapped(self._c_getitem, 100)

    @lazy
    def __getattr__(self):
        # cache it
        return lru_wrapped(self._c_getattr, 100)

    @lazy
    def _setit(self):
        return self._stuf.__setitem__

