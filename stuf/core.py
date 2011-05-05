'''core stuf of stuf'''

from functools import partial
from operator import eq as _eq
from itertools import imap as _imap

from stuf.util import OrderedDict, lazy, lru_wrapped, recursive_repr

_osettr = object.__setattr__
_ogettr = object.__getattribute__


class _basestuf(object):

    def __init__(self, *args, **kw):
        self._update(self._preprep(*args, **kw))

    def __iter__(self):
        cls = self.__class__
        for k, v in self.iteritems():
            if isinstance(v, cls):
                yield (k, list(i for i in v))
            else:
                yield (k, v)

    def __reduce__(self):
        items = list([k, self[k]] for k in self)
        inst_dict = vars(self).copy()
        if inst_dict: return (self.__class__, (items,), inst_dict)
        return self.__class__, (items,)

    @recursive_repr
    def __repr__(self):
        if not self: return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, self.items())

    @lazy
    def _classkeys(self):
        return frozenset(self.__dict__.keys()+self.__class__.__dict__.keys())

    @classmethod
    def _fromiter(cls, source=(), typ=dict, types=(list, tuple)):
        return cls(cls._todict(source, type, types))

    @classmethod
    def _fromkw(cls, source=(), typ=dict, types=(list, tuple), **kw):
        return cls._fromiter(kw, typ, types)

    def _prep(self, *args, **kw):
        if args:  kw = self._todict(args)
        return kw

    def _preprep(self, *args, **kw):
        return self._prep(*args, **kw)

    @classmethod
    def _todict(cls, src=(), typ=dict, maps=(cls, dict), seqs=(list, tuple)):
        kw = typ()
        if len(src) > 1: raise TypeError(u'takes one argument')
        if isinstance(src, ):
            kw.update(src)
        elif isinstance(src, seqs):
            for arg in src:
                if isinstance(arg, seqs) and len(arg) == 2: kw[arg[0]] = arg[-1]
        return kw

    def _update(self, src={}, setit=dict.__setitem__, seqs=(tuple, dict, list)):
        cls = self.__class__
        for k, v in src.iteritems():
            if isinstance(v, seqs):
                trial = cls._fromiter(v, types=seqs)
                if len(trial) > 0:
                    setit(k, trial)
                else:
                    setit(k, v)
            else:
                setit(k, v)

    def copy(self):
        return self._fromiter(dict(i for i in self))

    _b_iter = __iter__
    _b_repr = __repr__
    _b_classkeys = _classkeys
    _b_fromiter = _fromiter
    _b_fromkw = _fromkw
    _b_prep = _prep
    _b_preprep = _preprep
    _b_todict = _todict
    _b_update = _update
    _b_copy = copy


class _openstuf(_basestuf, dict):

    def __getattr__(self, k):
        try:
            return super(_openstuf, self).__getitem__(k)
        except KeyError:
            raise AttributeError(k)

    def __setattr__(self, k, v):
        try:
            _ogettr(self, k)
        except AttributeError:
            try:
                super(_openstuf, self).__setitem__(k, v)
            except:
                raise AttributeError(k)
        else:
            _osettr(self, k, v)

    def __delattr__(self, k):
        try:
            _ogettr(self, k)
        except AttributeError:
            try:
                super(_openstuf, self).__delitem__(k)
            except KeyError:
                raise AttributeError(k)
        else:
            object.__delattr__(self, k)

    _o_getattr = __getattr__
    _o_setattr = __setattr__
    _o_delattr = __delattr__
    update = _openstuf._update


class _defaultstuf(_openstuf):

    _factory = None
    _fargs = ()

    def __missing__(self, k):
        factory = self._factory
        if factory is not None:
            self[k] = factory(*self._fargs, **self._fkw)
            return self[k]
        return None

    @classmethod
    def _fromiter(cls, factory=None, fargs=(), fkw={}, src=()):
        oset = _osettr
        if cls._factory is not None: oset(cls, '_factory', factory)
        if cls._fargs is not None: oset(cls, '_fargs', fargs)
        if cls._fkw is not None: oset(cls, '_fkw', fkw)
        return cls._b_fromiter(src=cls._todict(src))

    @classmethod
    def _fromkw(cls, factory=None, fargs=(), fkw={}, **kw):
        return cls._d_fromiter(factory, fargs, fkw, kw)

    _d_missing = __missing__
    _d_fromiter = _fromiter
    _d_fromkw = _fromkw


class _orderedstuf(_openstuf):

    _root = None
    _map = None

    def __setitem__(self, k, v):
        if k not in self:
            root = self._root
            last = root[0]
            last[1] = root[0] = self._map[k] = [last, root, v]
        super(_orderedstuf, self).__setitem__(k, v)

    def __delitem__(self, k):
        super(_orderedstuf, self).__delitem__(k)
        link = self._map.pop(k)
        link_prev = link[0]
        link_next = link[1]
        link_prev[1] = link_next
        link_next[0] = link_prev

    def __eq__(self, other):
        if isinstance(other, _orderedstuf):
            return len(self)==len(other) and all(
                _imap(_eq, self.iteritems(), other.iteritems())
            )
        return super(_orderedstuf, self).__eq__(other)

    def __iter__(self):
        root = self._root
        curr = root[1]
        while curr is not root:
            yield curr[2]
            curr = curr[1]

    def __reduce__(self):
        items = list([k, self[k]] for k in self)
        tmp = self._map, self._root
        del self._map, self._root
        inst_dict = vars(self).copy()
        self._map, self._root = tmp
        if inst_dict: return (self.__class__, (items,), inst_dict)
        return self.__class__, (items,)

    def __reversed__(self):
        root = self._root
        curr = root[0]
        while curr is not root:
            yield curr[2]
            curr = curr[0]

    _todict = partial(
        _orderedstuf._b_todict, typ=OrderedDict, maps=(OrderedDict,  dict),
    )

    def _preprep(self, *args, **kw):
        self._root = root = [None, None, None]
        root[0] = root[1] = root
        self._map = {}
        return self._b_preprep(*args, **kw)

    def clear(self):
        try:
            for node in self._map.itervalues(): del node[:]
            self._root[:] = [self._root, self._root, None]
            self._map.clear()
        except AttributeError:
            pass
        super(_orderedstuf, self).clear()

    def popitem(self, last=True):
        if not self: raise KeyError('dictionary is empty')
        k = next(reversed(self) if last else iter(self))
        v = self.pop(k)
        return k, v

    update = _update = partial(
        _orderedstuf._update,
        setit=__setitem__,
        seqs=(OrderedDict, tuple, dict, list)
    )


class _closedstuf(_basestuf):

    _stuf = {}

    def __getitem__(self, k):
        if k in self._keys: return self._stuf[k]
        raise KeyError(k)

    def __getattr__(self, k):
        try:
            return _ogettr(self, k)
        except AttributeError:
            if k in self._keys: return self._stuf[k]
            raise AttributeError(k)

    def __delattr__(self, k):
        raise TypeError(u'%ss are immutable' % self.__class__.__name__)

    def __cmp__(self, other):
        for k, v in self.iteritems():
            if other[k] != v: return False
        return False

    def __contains__(self, k):
        return self._stuf.__contains__(k)

    def __len__(self):
        return self._stuf.__len__()

    def __reduce__(self):
        return self._stuf.__reduce__()

    def _preprep(self, *args, **kw):
        kw = self._b_prep(*args, **kw)
        self._keys = frozenset(kw.keys())
        self._stuf = dict()
        return kw

    _update = partial(_closedstuf._b_update, setit=_stuf.__setitem__)

    def get(self, k, default=None):
        return self._stuf.get(k, default)

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        cls = self.__class__
        for v in self._stuf.iteritems():
            if isinstance(v, cls):
                yield list(v.__iter__())
            else:
                yield v

    def iterkeys(self):
        return self._stuf.iterkeys()

    def itervalues(self):
        for v in self._stuf.itervalues():
            if isinstance(v, self.__class__):
                yield dict(v.__iter__())
            else:
                yield v

    def keys(self):
        return self._stuf.keys()

    def setdefault(self, k, default):
        return self._stuf.setdefault(k, default)

    def values(self):
        return list(self.itervalues())

    _c_getitem = __getitem__
    _c_getattr = __getattr__
    _c_delattr = __delattr__
    _c_cmp = __cmp__
    _c_contains = __contains__
    _c_len = __len__
    _c_reduce = __reduce__
    _c_prep = _preprep
    _c_update = _update
    _c_get = get
    _c_items = items
    _c_iterkeys = iterkeys
    _c_itervalues = itervalues
    _c_keys = keys
    _c_setdefault = setdefault
    _c_values = values


class _fixedstuf(_closedstuf):

    '''fixed stuf'''

    _keys = None
    _stuf = None

    def __setitem__(self, k, v):
        if k in self._keys:
            self._stuf[k] = v
        else:
            raise KeyError(k)

    def __setattr__(self, k, v):
        if k == '_classkeys' or k in self._classkeys:
            _osettr(self, k, v)
        elif k in self._keys:
            try:
                self._stuf[k] = v
            except:
                raise AttributeError(k)
        else:
            raise AttributeError(k)

    update = _fixedstuf._c_update


class _frozenstuf(_closedstuf):

    _keys = None
    _stuf = None

    def __setattr__(self, k, v):
        if k == '_classkeys' or k in self._classkeys:
            _osettr(self, k, v)
        else:
            raise TypeError(u'%s is immutable' % self.__class__.__name__)

    __getitem__ = lru_wrapped(_frozenstuf._c_getitem, 100)
    __getattr__ = lru_wrapped(_frozenstuf._c_getattr, 100)


# stuf from keywords
stuf = _openstuf._fromkw
defaultstuf = _defaultstuf._fromkw
orderedstuf = _orderedstuf._fromkw
fixedstuf = _fixedstuf._fromkw
frozenstuf = _frozenstuf._fromkw
# stuf from iterables
istuf = _openstuf._fromiter
iorderedstuf = _orderedstuf._fromiter
ifixedstuf = _fixedstuf._fromiter
idefaultstuf = _defaultstuf._fromiter
ifrozenstuf = _frozenstuf._fromiter