# -*- coding: utf-8 -*-
'''core stuf'''

from __future__ import absolute_import

from .base import basestuf 


class stuf(basestuf, dict):

    '''dictionary with dot attributes'''

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)

    def __setattr__(self, k, v):
        # handle normal object attributes
        if k == '_classkeys' or k in self._classkeys:
            object.__getattribute__(self, k, v)
        # handle special attributes
        else:
            try:
                self[k] = v
            except:
                raise AttributeError(k)

    def __delattr__(self, k):
        # allow deletion of key-value pairs only
        if not k == '_classkeys' or k in self._classkeys:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)
