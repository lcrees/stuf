# -*- coding: utf-8 -*-
'''core stuf'''

from __future__ import absolute_import

from .util import lazy
from .base import basestuf 


class stuf(basestuf, dict):

    '''dictionary with dot attributes'''

    def __getattr__(self, k):
        try:
            return self.__getitem__(k)
        except KeyError:
            raise AttributeError(k)

    def __setattr__(self, k, v):
        # handle normal object attributes
        if k == '_classkeys' or k in self._classkeys:
            object.__getattribute__(self, k, v)
        # handle special attributes
        else:
            try:
                self.__setitem__(k, v)
            except:
                raise AttributeError(k)

    def __delattr__(self, k):
        # allow deletion of key-value pairs only
        if not k == '_classkeys' or k in self._classkeys:
            try:
                self.__delitem__(k)
            except KeyError:
                raise AttributeError(k)

    @lazy
    def update(self):
        # public version of _Basestuf._update
        return self._update
