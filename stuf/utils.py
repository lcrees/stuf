# -*- coding: utf-8 -*-
'''stuf utilities'''

import re
from threading import Lock
from unicodedata import normalize
from importlib import import_module
from functools import update_wrapper

from stuf.six import items, isstring, u


def lazyimport(path, attribute=None, i=import_module, g=getattr, s=isstring):
    '''
    Deferred module loader.

    :argument path: something to load
    :keyword str attribute: attribute on loaded module to return
    '''
    if s(path):
        try:
            dot = path.rindex('.')
            # import module
            path = g(i(path[:dot]), path[dot + 1:])
        # If nothing but module name, import the module
        except (AttributeError, ValueError):
            path = i(path)
        if attribute:
            path = g(path, attribute)
    return path


def lru(maxsize=100):
    '''
    Least-recently-used cache decorator.

    If *maxsize* is set to None, the LRU features are disabled and the cache
    can grow without bound.

    Arguments to the cached function must be hashable.

    Access the underlying function with f.__wrapped__.

    See:  http://en.wikipedia.org/wiki/Cache_algorithms#Least_Recently_Used

    By Raymond Hettinger
    '''

    # Users should only access the lru through its public API:
    #   f.__wrapped__
    # The internals of the lru are encapsulated for thread safety and
    # to allow the implementation to change (including a possible C version).

    def decorating_function(user_function):
        cache = dict()
        items_ = items
        repr_ = repr
        intern_ = intern
        # bound method to lookup key or return None
        cache_get = cache.get
        # localize the global len() function
        len_ = len
        # because linkedlist updates aren't threadsafe
        lock = Lock()
        # root of the circular doubly linked list
        root = []
        # make updateable non-locally
        nonlocal_root = [root]
        # initialize by pointing to self
        root[:] = [root, root, None, None]
        # names for the link fields
        PREV, NEXT, KEY, RESULT = 0, 1, 2, 3

        if maxsize is None:
            def wrapper(*args, **kw):
                # simple caching without ordering or size limit
                key = repr_(args, items_(kw)) if kw else repr_(args)
                # root used here as a unique not-found sentinel
                result = cache_get(key, root)
                if result is not root:
                    return result
                result = user_function(*args, **kw)
                cache[intern_(key)] = result
                return result
        else:
            def wrapper(*args, **kw):
                # size limited caching that tracks accesses by recency
                key = repr_(args, items_(kw)) if kw else repr_(args)
                with lock:
                    link = cache_get(key)
                    if link is not None:
                        # record recent use of the key by moving it to the
                        # front of the list
                        root, = nonlocal_root
                        link_prev, link_next, key, result = link
                        link_prev[NEXT] = link_next
                        link_next[PREV] = link_prev
                        last = root[PREV]
                        last[NEXT] = root[PREV] = link
                        link[PREV] = last
                        link[NEXT] = root
                        return result
                result = user_function(*args, **kw)
                with lock:
                    root = nonlocal_root[0]
                    if len_(cache) < maxsize:
                        # put result in a new link at the front of the list
                        last = root[PREV]
                        link = [last, root, key, result]
                        cache[intern_(key)] = last[NEXT] = root[PREV] = link
                    else:
                        # use root to store the new key and result
                        root[KEY] = key
                        root[RESULT] = result
                        cache[intern_(key)] = root
                        # empty the oldest link and make it the new root
                        root = nonlocal_root[0] = root[NEXT]
                        del cache[root[KEY]]
                        root[KEY] = None
                        root[RESULT] = None
                return result

        wrapper.__wrapped__ = user_function
        return update_wrapper(wrapper, user_function)

    return decorating_function


class Sluggify(object):

    _first = staticmethod(re.compile('[^\w\s-]').sub)
    _second = staticmethod(re.compile('[-\s]+').sub)

    def __call__(self, value):
        '''
        normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens
        '''
        return self._second('-', u(self._first(
            '', normalize('NFKD', u(value)).encode('ascii', 'ignore')
        ).strip().lower()))


lru_wrapped = lru
sluggify = Sluggify()
