'''stuf'''

from inspect import ismethod
try:
    from collections import OrderedDict
except ImportError:
    from stuf.compat import OrderedDict

from stuf.util import lru_cache


#class _frozenstuf(type):
#
#    def __new__(cls, name, base, classdict):
#        def __init__(self, **kw):
#            for k, v in kw.iteritems(): setattr(self, k, v)
#        def __getattr__(self, k):
#            return object.__getattribute__(self, k)
#        @lru_cache()
#        def __getitem__(self, k):
#            return self.__getattr__(k)
#        def __setattr__(self, k, v):
#            object.__setattr__(self, k, v)
#        def __repr__(self):
#            return '%s(%r)' % (
#                self.__class__.__name__,
#                ', '.join(list('%s=%r' % (k, getattr(self, k))
#                    for k in self.__slots__
#                ))
#            )
#        newdict = dict(
#            (k, v) for k, v in locals().iteritems() if k.startswith('__')
#        )
#        newdict['__slots__'] = classdict.keys() + newdict.keys()
#        obj = type.__new__(cls, name, base, newdict)
#        return obj


#class frozenstuf(object):
#
#    def __new__(cls, *arg, **kw):
##        if arg:
##            if isinstance(arg[0], dict):
##                if len(arg) > 1: raise TypeError('Invalid number of arguments')
##                kw.update(dict(**arg))
##            elif isinstance(arg, (list, tuple)):
##                kw.update(**dict((k, v) for k, v in arg))
##        kw.update(dict(
##            (k, v) for k, v in cls.__dict__.iteritems()
##            if not k.startswith('__dict')
##        ))
##        obj = _frozenstuf(cls.__name__, (object, ), kw)
##        return obj(**kw)
#        def namedtuple(typename, field_names, verbose=False, rename=False):
#            """Returns a new subclass of tuple with named fields.
#
#            >>> Point = namedtuple('Point', 'x y')
#            >>> Point.__doc__                   # docstring for the new class
#            'Point(x, y)'
#            >>> p = Point(11, y=22)             # instantiate with positional args or keywords
#            >>> p[0] + p[1]                     # indexable like a plain tuple
#            33
#            >>> x, y = p                        # unpack like a regular tuple
#            >>> x, y
#            (11, 22)
#            >>> p.x + p.y                       # fields also accessable by name
#            33
#            >>> d = p._asdict()                 # convert to a dictionary
#            >>> d['x']
#            11
#            >>> Point(**d)                      # convert from a dictionary
#            Point(x=11, y=22)
#            >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
#            Point(x=100, y=22)
#
#            """
#
#            # Parse and validate the field names.  Validation serves two purposes,
#            # generating informative error messages and preventing template injection attacks.
#            if isinstance(field_names, basestring):
#                field_names = field_names.replace(',', ' ').split() # names separated by whitespace and/or commas
#            field_names = tuple(map(str, field_names))
#            if rename:
#                names = list(field_names)
#                seen = set()
#                for i, name in enumerate(names):
#                    if (not all(c.isalnum() or c=='_' for c in name) or _iskeyword(name)
#                        or not name or name[0].isdigit() or name.startswith('_')
#                        or name in seen):
#                        names[i] = '_%d' % i
#                    seen.add(name)
#                field_names = tuple(names)
#            for name in (typename,) + field_names:
#                if not all(c.isalnum() or c=='_' for c in name):
#                    raise ValueError('Type names and field names can only contain alphanumeric characters and underscores: %r' % name)
#                if _iskeyword(name):
#                    raise ValueError('Type names and field names cannot be a keyword: %r' % name)
#                if name[0].isdigit():
#                    raise ValueError('Type names and field names cannot start with a number: %r' % name)
#            seen_names = set()
#            for name in field_names:
#                if name.startswith('_') and not rename:
#                    raise ValueError('Field names cannot start with an underscore: %r' % name)
#                if name in seen_names:
#                    raise ValueError('Encountered duplicate field name: %r' % name)
#                seen_names.add(name)
#
#            # Create and fill-in the class template
#            numfields = len(field_names)
#            argtxt = repr(field_names).replace("'", "")[1:-1]   # tuple repr without parens or quotes
#            reprtxt = ', '.join('%s=%%r' % name for name in field_names)
#            template = '''class %(typename)s(tuple):
#                '%(typename)s(%(argtxt)s)' \n
#                __slots__ = () \n
#                _fields = %(field_names)r \n
#                def __new__(_cls, %(argtxt)s):
#                    'Create new instance of %(typename)s(%(argtxt)s)'
#                    return _tuple.__new__(_cls, (%(argtxt)s)) \n
#                @classmethod
#                def _make(cls, iterable, new=tuple.__new__, len=len):
#                    'Make a new %(typename)s object from a sequence or iterable'
#                    result = new(cls, iterable)
#                    if len(result) != %(numfields)d:
#                        raise TypeError('Expected %(numfields)d arguments, got %%d' %% len(result))
#                    return result \n
#                def __repr__(self):
#                    'Return a nicely formatted representation string'
#                    return '%(typename)s(%(reprtxt)s)' %% self \n
#                def _asdict(self):
#                    'Return a new OrderedDict which maps field names to their values'
#                    return OrderedDict(zip(self._fields, self)) \n
#                def _replace(_self, **kwds):
#                    'Return a new %(typename)s object replacing specified fields with new values'
#                    result = _self._make(map(kwds.pop, %(field_names)r, _self))
#                    if kwds:
#                        raise ValueError('Got unexpected field names: %%r' %% kwds.keys())
#                    return result \n
#                def __getnewargs__(self):
#                    'Return self as a plain tuple.  Used by copy and pickle.'
#                    return tuple(self) \n\n''' % locals()
#            for i, name in enumerate(field_names):
#                template += "        %s = _property(_itemgetter(%d), doc='Alias for field number %d')\n" % (name, i, i)
#            if verbose:
#                print template
#
#            # Execute the template string in a temporary namespace and
#            # support tracing utilities by setting a value for frame.f_globals['__name__']
#            namespace = dict(_itemgetter=_itemgetter, __name__='namedtuple_%s' % typename,
#                             OrderedDict=OrderedDict, _property=property, _tuple=tuple)
#            try:
#                exec template in namespace
#            except SyntaxError, e:
#                raise SyntaxError(e.message + ':\n' + template)
#            result = namespace[typename]
#
#            # For pickling to work, the __module__ variable needs to be set to the frame
#            # where the named tuple is created.  Bypass this step in enviroments where
#            # sys._getframe is not defined (Jython for example) or sys._getframe is not
#            # defined for arguments greater than 0 (IronPython).
#            try:
#                result.__module__ = _sys._getframe(1).f_globals.get('__name__', '__main__')
#            except (AttributeError, ValueError):
#                pass
#
#            return result


class stuf(dict):

    '''stuf'''

    def __init__(self, *args, **kw):
        super(stuf, self).__init__()
        if args:
            if len(args) > 1:
                raise TypeError('Invalid number of arguments %s' % len(args))
            source = args[0]
            if isinstance(source, dict):
                kw.update(source)
            elif isinstance(source, (list, tuple)):
                for arg in source:
                    if isinstance(arg, (list, tuple)) and len(arg) == 2:
                        if isinstance(arg[-1], (tuple, dict, list)):
                            self[arg[0]] = self.__class__(arg[-1])
                        else:
                            self[arg[0]] = arg[-1]
        if kw:
            for k, v in kw.iteritems():
                if isinstance(v, (tuple, dict, list)):
                    trial = self.__class__(v)
                    if len(trial) > 0:
                        self[k] = trial
                    else:
                        self[k] = v
                else:
                    self[k] = v

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)

    def __setattr__(self, k, v):
        try:
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                self[k] = v
            except:
                raise AttributeError(k)
        else:
            object.__setattr__(self, k, v)

    def __delattr__(self, k):
        try:
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)
        else:
            object.__delattr__(self, k)

    def __iter__(self):
        for k, v in self.iteritems(): yield (k, tuple(v.__iter__()))

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, dict(self))


class defaultstuf(stuf):

    _fargs = ()

    def __init__(self, factory, *args, **kw):
        super(defaultstuf, self).__init__()
        self._factory = factory
        if args: self._fargs = args[0]
        fullargs = args[1:]
        if fullargs:
            if len(fullargs) > 1:
                raise TypeError('Invalid number of arguments %s' % len(args))
            source = fullargs[0]
            if isinstance(source, dict):
                kw.update(source)
            elif isinstance(source, (list, tuple)):
                for arg in source:
                    if isinstance(arg, (list, tuple)) and len(arg) == 2:
                        if isinstance(arg[-1], (tuple, dict, list)):
                            self[arg[0]] = self.__class__(
                                factory, self._fargs, arg[-1],
                            )
                        else:
                            self[arg[0]] = arg[-1]
        if kw:
            for k, v in kw.iteritems():
                if isinstance(v, (tuple, dict, list)):
                    trial = self.__class__(factory, self._fargs, v)
                    if len(trial) > 0:
                        self[k] = trial
                    else:
                        self[k] = v
                else:
                    self[k] = v

    def __getattr__(self, k):
        if k in self._methods:
            return object.__getattribute__(self, k)
        else:
            try:
                return self[k]
            except KeyError:
                raise AttributeError(k)

    def __setattr__(self, k, v):
        if k in self._methods:
            object.__setattr__(self, k, v)
        else:
            try:
                self[k] = v
            except:
                raise AttributeError(k)

    def __delattr__(self, k):
        if k in self._methods:
            object.__delattr__(self, k)
        else:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)

    def __missing__(self, key):
        self[key] = self._factory(*self._fargs)
        return self[key]

    @property
    def _methods(self):
        return frozenset(list(
            k for k, v in self.__dict__.iteritems() if ismethod(v)
        )+['_factory', '_fargs'])


class orderedstuf(OrderedDict):

    def __init__(self, *args, **kw):
        super(orderedstuf, self).__init__(self)
        if args:
            if len(args) > 1:
                raise TypeError('Invalid number of arguments %s' % len(args))
            source = args[0]
            if isinstance(args, OrderedDict):
                for k in args:
                    v = args[k]
                    if isinstance(v, (tuple, dict, list, OrderedDict)):
                        trial = self.__class__(v)
                        if len(trial) > 0:
                            self[k] = trial
                        else:
                            self[k] = v
                    else:
                        self[k] = v
            elif isinstance(source, dict):
                kw.update(source)
            elif isinstance(source, (list, tuple)):
                for arg in args:
                    if isinstance(arg, (list, tuple)) and len(arg) == 2:
                        if isinstance(
                            arg[-1], (tuple, dict, list, OrderedDict)
                        ):
                            self[arg[0]] = self.__class__(arg[-1])
                        else:
                            self[arg[0]] = arg[-1]
        if kw:
            for k, v in kw.iteritems():
                if isinstance(v, (tuple, dict, list, OrderedDict)):
                    trial = self.__class__(v)
                    if len(trial) > 0:
                        self[k] = trial
                    else:
                        self[k] = v
                else:
                    self[k] = v

    def __getattr__(self, k):
        if k in self._methods:
            return object.__getattribute__(self, k)
        else:
            try:
                return self[k]
            except KeyError:
                raise AttributeError(k)

    def __setattr__(self, k, v):
        if k in self._methods:
            object.__setattr__(self, k, v)
        else:
            try:
                self[k] = v
            except:
                raise AttributeError(k)

    def __delattr__(self, k):
        if k in self._methods:
            object.__delattr__(self, k)
        else:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

    @property
    def _methods(self):
        first = ['__map', '__root'] + list(
            k for k, v in self.__dict__.iteritems() if ismethod(v)
        )
        first += list('_OrderedDict'+k for k in first)
        return frozenset(first)