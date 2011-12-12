# -*- coding: utf-8 -*-
'''basestuf stuf'''

from collections import Mapping, Sequence

from stuf.util import lazy, recursive_repr, class_name


class basestuf(object):

    '''stuf basestuf'''
    
    _mapping = dict

    def __init__(self, *args, **kw):
        '''
        @param *args: iterable of keys/value pairs
        @param **kw: keyword arguments
        '''
        self.update(*args, **kw)
        
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
        return self._build(state)

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

    def _prepare(self, *args, **kw):
        '''
        preps stuff for stuf object construction

        @param arg: iterable sequence
        '''
        kw.update(self._build(args))
        return kw
    
    def _populate(self, iterable):
        '''
        converts stuff into stuf key/attrs and values

        @param iterable: source mapping object
        @param sq: sequence of types to check
        '''
        prepare = self._prepare
        for k, v in iterable.iteritems():
            if isinstance(v, Sequence):
                # see if stuf can be converted to nested stuf
                trial = prepare(iterable)
                if len(trial) > 0:
                    self[k] = trial
                else:
                    self[k] = v
            else:
                self[k] = v 

    def _build(self, iterable):
        '''
        converts stuff into some sort of mapping

        @param iterable: iterable stuff
        '''
        kind = self._mapping
        # add class to handle potential nested objects of the same class
        kw = kind()
        if isinstance(iterable, Mapping):
            kw.update(iterable)
        elif isinstance(iterable, Sequence):
            # extract appropriate key-values from sequence
            for arg in iterable:
                if isinstance(arg, (Sequence, self.__class__)) and len(arg) == 2: 
                    kw[arg[0]] = arg[-1]
        return kw

    def update(self, *args, **kw):
        '''updates stuf with iterables and keyword arguments'''
        self._populate(self._prepare(*args, **kw))

    def copy(self):
        return self._build(dict(i for i in self))
