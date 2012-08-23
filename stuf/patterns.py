# -*- coding: utf-8 -*-
'''stuf search.'''

import sys
import traceback
from os import sep
from functools import partial
from collections import namedtuple

from stuf.utils import lru
from stuf.core import stuf
from stuf.base import first, docit
from stuf.deep import recursive_repr
from parse import compile as pcompile
from stuf.six.moves import filterfalse  # @UnresolvedImport
from stuf.iterable import exhaustitems, exhauststar
from stuf.six import StringIO, isstring, filter, map, rcompile, rescape, rsub


def globpattern(expr):
    '''Translate glob `expr` to regular expression.'''
    i, n = 0, len(expr)
    res = []
    rappend = res.append
    while i < n:
        c = expr[i]
        i += 1
        if c == '*':
            rappend('(.*)')
        elif c == '?':
            rappend('(.)')
        elif c == '[':
            j = i
            if j < n and expr[j] == '!':
                j += 1
            if j < n and expr[j] == ']':
                j += 1
            while j < n and expr[j] != ']':
                j += 1
            if j >= n:
                rappend('\\[')
            else:
                stuff = expr[i:j].replace('\\', '\\\\')
                i = j + 1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                rappend('[{0}]'.format(stuff))
        else:
            rappend(rescape(c))
    rappend('\Z(?ms)')
    return rsub(
        r'((?<!\\)(\\\\)*)\.',
        r'\1[^{0}]'.format(r'\\\\' if sep == '\\' else sep),
        r''.join(res),
    )


# regular expression search
regex = lambda expr, flag: rcompile(expr, flag).search
# parse search
parse = lambda expr, flag: pcompile(expr)._search_re.search
# glob search
glob = lambda expr, flag: rcompile(globpattern(expr), flag).search
# search dictionary
SEARCH = dict(parse=parse, glob=glob, regex=regex)


@lru()
def searcher(expr, flags=32):
    '''Build search function from `expr`.'''
    try:
        scheme, expr = expr.split(':', 1) if isstring(expr) else expr
        return SEARCH[scheme](expr, flags)
    except KeyError:
        raise TypeError('"{0}" is invalid search scheme'.format(scheme))


def truthexcept(call, doc):
    def test(call, data):
        try:
            call(data)
            return True
        except:
            return False
    return docit(partial(test, call), doc)


def truthpattern(expr, doc, flags=32):
    return docit(partial(lambda x, y: bool(x(y)), searcher(expr, flags)), doc)


def error(info, this, tb=False):
    if not tb:
        raise Untrue('value must be {0}, got {r} instead'.format(
            info, recursive_repr(this),
        ))
    with StringIO() as sio:
        tb = sys.exc_info()
        traceback.print_exception(tb[0], tb[1], tb[2], None, sio)
        s = sio.getvalue()
    raise Untrue(
        'value must be {0} but got {r} with exception {2} instead'.format(
            info, recursive_repr(this), s[:-1] if s[-1:] == '\n' else s,
        )
    )


def change(call, doc=None, info=None, default=None, tb=False, **kw):
    def change(call, err, this, default=None):
        try:
            return call(this)
        except:
            if default is not None:
                return default
            err(this)
    return docit(
        partial(
            change,
            partial(call, **kw),
            partial(error, info, tb=tb),
            default=default,
        ),
        doc,
    )


def truth(call, doc=None, info=None, default=None, tb=False, cmp=None):
    def truth(call, err, this, default=None):
        try:
            if call(this):
                return this
        except:
            if default is not None:
                return default
            err(this)
    if cmp is not None:
        call = partial(call, cmp)
    return docit(
        partial(truth, call, partial(error, info, tb=tb), default=default), doc
    )


def detect(patterns):
    '''Match item in sequence with pattern in `patterns`.'''
    return partial(
        lambda y, x: any(p(first(x)) for p in y),
        tuple(map(searcher, patterns)),
    )


# run multiple callables on one value to verify truth
gauntlet = lambda tests, this: all(test(this) for test in tests)


def _clude(filter, default, patterns):
    '''Create filter from `patterns`.'''
    if not patterns:
        # trivial case: *clude everything
        return default
    patterns = tuple(map(searcher, patterns))
    # handle general case for *clusion
    return partial(filter, lambda x: any(p(x) for p in patterns))


# filter for exclusion `patterns`.
exclude = partial(_clude, filterfalse, lambda x: x)
# filter for inclusion `patterns`.
include = partial(_clude, filter, lambda x: x[0:0])


def fixed(tests, these):
    '''Change sequence `these` to correct output with `tests`.'''
    results = Fixed(these, [], [])
    tappend = results.true.append
    fappend = results.false.append
    def closure(idx, test): #@IgnorePep8
        try:
            tappend(test(tests[idx]))
            fappend(TRUTH)
        except Untrue as e:
            tappend(UNTRUTH)
            fappend(e)
    exhauststar(closure, enumerate(tests))
    return results


def named(tests, these):
    '''Change mapping `these` to correct output with `tests`.'''
    results = Named(these, stuf(), stuf())
    tsetitem = results.true.__setitem__
    fsetitem = results.false.__setitem__
    def closure(k, v): #@IgnorePep8
        try:
            tsetitem(k, v(these[k]))
            fsetitem(k, TRUTH)
        except Untrue as e:
            tsetitem(k, UNTRUTH)
            fsetitem(k, e)
    exhaustitems(closure, tests)
    return results


class Untrue(Exception):
    '''Data is untrue.'''


# truth marker
TRUTH = hash('TRUTH')
# untruth marker
UNTRUTH = hash('UNTRUTH')
# fixed values
Fixed = namedtuple('Fixed', 'these true false')
# named values
Named = namedtuple('Named', 'these true false')
