# -*- coding: utf-8 -*-
'''basestuf stuf'''

from collections import Mapping, Sequence

from stuf.util import lazy, recursive_repr, class_name


class basestuf(object):

    '''stuf basestuf'''
    
    _mapping = dict

    def __init__(self, arg=None, **kw):
        '''
        @param arg: iterable of keys, values
        '''
        if arg is None:
            arg = kw
        else:
            self._tomapping(arg)
        self._convert(self._preprepare(arg))
        
    def __iter__(self):
        cls = self.__class__
        for k, v in self.iteritems(): ##pylint: disable-msg=e1101
            # nested stuf of some sort
            if isinstance(v, cls):
                yield (k, dict(i for i in v))
            # normal key, value pair
            else:
                yield (k, v)

    def __getstate__(self):
        return dict(i for i in self)

    def __setstate__(self, state):
        return self._tomapping(state)

    @recursive_repr
    def __repr__(self):
        if not self: 
            return '%s()' % class_name(self) 
        return '%s(%r)' % (class_name(self), self.items()) ##pylint: disable-msg=e1101

    @lazy
    def _classkeys(self):
        '''protected keywords'''
        return frozenset(
            vars(self).keys()+self.__class__.__dict__.keys()+[
                '_keys', '_factory', '_fargs', '_fkw', '_root', '_map',
            ]
        )

    @lazy
    def _setit(self):
        '''hidden setitem, crouching setter'''
        return self.__setitem__ ##pylint: disable-msg=e1101

    def _prep(self, arg, **kw):
        '''
        preps stuff for stuf object construction

        @param arg: iterable sequence
        '''
        # make iterable sequence into dictionary
        if arg: 
            kw.update(self._tomapping(arg))
        return kw

    def _preprepare(self, arg):
        '''
        preps stuff for stuf insertion

        @param arg: iterable sequence
        '''
        return arg
    
    def _convert(self, iterable):
        '''
        converts stuff into stuf key/attrs and values

        @param iterable: source mapping object
        @param sq: sequence of types to check
        '''
        setit = self._setit
        prepare = self._tomapping
        for k, v in iterable.iteritems():
            if isinstance(v, Sequence):
                # see if stuf can be converted to nested stuf
                trial = prepare(iterable)
                if len(trial) > 0:
                    setit(k, trial) ##pylint: disable-msg=e1121
                else:
                    setit(k, v) ##pylint: disable-msg=e1121
            else:
                setit(k, v) ##pylint: disable-msg=e1121

    def _tomapping(self, iterable):
        '''
        converts stuff into some sort of mapping

        @param iterable: iterable stuff
        '''
        kind = self._mapping
        # add class to handle potential nested objects of the same class
        kw = kind()
        if isinstance(iterable, Mapping):
            kw.update(kind(i for i in iterable.iteritems()))
        elif isinstance(iterable, Sequence):
            # extract appropriate key-values from sequence
            for arg in iterable:
                if isinstance(arg, (Sequence, self.__class__)) and len(arg) == 2: 
                    kw[arg[0]] = arg[-1]
        return kw

    def _update(self, *args, **kw):
        '''updates stuf with iterables and keywor arguments'''
        return self._convert(self._prep(*args, **kw))

    def copy(self):
        return self._tomapping(dict(i for i in self))
