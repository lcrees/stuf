# -*- coding: utf-8 -*-
'''stuf deep object utilities'''

from operator import itemgetter, attrgetter, getitem

from stuf.six import items, get_ident


def attr_or_item(this, key):
    '''
    get attribute or item

    @param this: object
    @param key: key to lookup
    '''
    try:
        return getitem(this, key)
    except KeyError:
        return getter(this, key)


def clsname(this):
    '''
    get class name

    @param this: object
    '''
    return getattr(this.__class__, '__name__')


def deepget(this, key, default=None):
    '''
    get an attribute with deep attribute path

    @param this: object
    @param key: key to lookup
    @param default: default value returned if key not found (default: None)
    '''
    try:
        return attrgetter(key)(this)
    except AttributeError:
        return default


def deleter(this, key):
    '''
    delete an attribute

    @param this: object
    @param key: key to lookup
    '''
    try:
        object.__delattr__(this, key)
    except (TypeError, AttributeError):
        delattr(this, key)


def getcls(this):
    '''
    get class of instance

    @param this: an instance
    '''
    return getter(this, '__class__')


def getter(this, key):
    '''
    get an attribute

    @param this: object
    @param key: key to lookup
    @param default: default value returned if key not found (default: None)
    '''
    try:
        return object.__getattribute__(this, key)
    except (AttributeError, TypeError):
        return getattr(this, key)


def getdefault(this, key, default=None):
    '''
    get an attribute

    @param this: object
    @param key: key to lookup
    @param default: default value returned if key not found (default: None)
    '''
    try:
        return getter(this, key)
    except AttributeError:
        return default


def instance_or_class(key, this, that):
    '''
    get attribute of an instance or class

    @param key: name of attribute to look for
    @param this: instance to check for attribute
    @param that: class to check for attribute
    '''
    try:
        return getter(this, key)
    except AttributeError:
        return getter(that, key)


def inverse_lookup(value, this, default=None):
    '''
    get attribute of an instance by value

    @param value: value to lookup as a key
    @param this: instance to check for attribute
    @param default: default key (default: None)
    '''
    try:
        return itemgetter(value)(
            dict((v, k) for k, v in items(vars(this)))
        )
    except (TypeError, KeyError):
        return default


def recursive_repr(this):
    '''
    Decorator to make a repr function return "..." for a recursive call

    @param this: object
    '''
    repr_running = set()
    def wrapper(self): #@IgnorePep8
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
    wrapper.__name__ = selfname(this)
    return wrapper


def selfname(this):
    '''
    get object name

    @param this: object
    '''
    return getter(this, '__name__')


def setter(this, key, value):
    '''
    set attribute

    @param this: object
    @param key: key to set
    @param value: value to set
    '''
    # it's an instance
    try:
        this.__dict__[key] = value
        return value
    # it's a class
    except TypeError:
        setattr(this, key, value)
        return value


def setdefault(this, key, default=None):
    '''
    get an attribute, creating and setting it if needed

    @param this: object
    @param key: key to lookup
    @param default: default value returned if key not found (default: None)
    '''
    try:
        return getter(this, key)
    except AttributeError:
        setter(this, key, default)
        return default


get_or_default = getdefault
