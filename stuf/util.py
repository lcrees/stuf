# -*- coding: utf-8 -*-
## pylint: disable-msg=w0702
'''stuf utilities'''

from functools import wraps

try:
    from thread import get_ident
except ImportError:
    from dummy_thread import get_ident
try:
    from collections import OrderedDict
except  ImportError:
    from ordereddict import OrderedDict


def lru_wrapped(this, maxsize=100):
    # order: least recent to most recent
    cache = OrderedDict()

    @wraps(this)
    def wrapper(*args, **kw):
        key = args
        if kw:
            key += tuple(sorted(kw.items()))
        try:
            result = cache.pop(key)
        except KeyError:
            result = this(*args, **kw)
            # purge least recently used cache entry
            if len(cache) >= maxsize:
                cache.popitem(0)
        # record recent use of this key
        cache[key] = result
        return result
    return wrapper


def class_name(this):
    '''
    get class name

    @param this: object
    '''
    return getattr(this.__class__, '__name__')


def object_name(this):
    '''
    get object name

    @param this: object
    '''
    return getattr(this, '__name__')


def recursive_repr(this):
    '''Decorator to make a repr function return "..." for a recursive call'''
    repr_running = set()

    def wrapper(self):
        key = id(self), get_ident()
        if key in repr_running:
            return '...'
        repr_running.add(key)
        try:
            result = this(self)
        finally:
            repr_running.discard(key)
        return result
    # Can't use functools.wraps() here because of bootstrap issues
    wrapper.__module__ = getattr(this, '__module__')
    wrapper.__doc__ = getattr(this, '__doc__')
    wrapper.__name__ = object_name(this)
    return wrapper


class lazybase(object):

    def __init__(self, method):
        self.method = method
        try:
            self.__doc__ = method.__doc__
            self.__module__ = method.__module__
            self.__name__ = object_name(method)
        except:
            pass


class lazy(lazybase):

    '''Lazily assign attributes on an instance upon first use.'''

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self.method(instance)
        object.__setattr__(instance, self.__name__, value)
        return value


class lazy_class(lazybase):

    '''Lazily assign attributes on an class upon first use.'''

    def __get__(self, instance, owner):
        value = self.method(owner)
        setattr(owner, self.__name__, value)
        return value
