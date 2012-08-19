# -*- coding: utf-8 -*-
'''stuf search.'''

import sys
import traceback
from os import sep
from functools import partial
from collections import namedtuple

from stuf.utils import lru
from stuf.core import stuf
from stuf.base import first, add_doc
from stuf.deep import recursive_repr
from parse import compile as pcompile
from stuf.six.moves import filterfalse  # @UnresolvedImport
from stuf.six import (
    StringIO, isstring, filter, map, rcompile, rescape, rsub, items)

regex = lambda expr, flag: rcompile(expr, flag).search
parse = lambda expr, flag: pcompile(expr)._search_re.search
glob = lambda expr, flag: rcompile(globpattern(expr), flag).search
gauntlet = lambda tests, this: all(test(this) for test in tests)
UNTRUTH = hash('UNTRUTH')
Fixed = namedtuple('Fixed', 'these true false')
Named = namedtuple('Named', 'these true false')
SEARCH = dict(parse=parse, glob=glob, regex=regex)


def detect(patterns):
    '''Create filter from inclusion `patterns`.'''
    patterns = tuple(map(searcher, patterns))
    return lambda x: any(p(first(x)) for p in patterns)


def exclude(patterns):
    '''Create filter from exclusion `patterns`.'''
    if not patterns:
        # trivial case: include everything
        return lambda x: x
    patterns = tuple(map(searcher, patterns))
    # handle general case for exclusion
    return partial(filterfalse, lambda x: any(p(x) for p in patterns))


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


def include(patterns):
    '''Create filter from inclusion `patterns`.'''
    if not patterns:
        # trivial case: exclude everything
        return lambda x: x[0:0]
    patterns = tuple(map(searcher, patterns))
    # handle general case for inclusion
    return partial(filter, lambda x: any(p(x) for p in patterns))


@lru()
def searcher(expr, flag=32):
    '''Build search function from `expr`.'''
    try:
        scheme, expr = expr.split(':', 1) if isstring(expr) else expr
        return SEARCH[scheme](expr, flag)
    except KeyError:
        raise TypeError('"{0}" is not a valid search scheme'.format(scheme))


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
        'value must be {0} but got {r} instead with exception {2}'.format(
            info, recursive_repr(this), s[:-1] if s[-1:] == '\n' else s,
        )
    )


def truthexcept(call, doc):
    def test(call, data):
        try:
            call(data)
            return True
        except:
            return False
    return add_doc(partial(test, call), doc)


def truthpattern(expr, doc, flags=32):
    return add_doc(
        partial(lambda x, y: bool(x(y)), rcompile(expr, flags).search), doc,
    )


def change(call, doc=None, info=None, default=None, tb=False, **kw):
    def change(call, err, this, default=None):
        try:
            return call(this)
        except:
            if default is not None:
                return default
            err(this)
    return add_doc(
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
    return add_doc(
        partial(truth, call, partial(error, info, tb=tb), default=default), doc
    )


def fixed(tests, these):
    results = Fixed(these, [], [])
    tappend = results.true.append
    fappend = results.false.append
    for idx, test in enumerate(tests):
        try:
            tappend(test(tests[idx]))
            fappend(False)
        except Untrue as e:
            tappend(UNTRUTH)
            fappend(e)
    return results


def named(tests, these):
    results = Named(these, stuf(), stuf())
    tsetitem = results.true.__setitem__
    fsetitem = results.false.__setitem__
    for k, v in items(tests):
        try:
            tsetitem(k, v(these[k]))
            fsetitem(k, False)
        except Untrue as e:
            tsetitem(k, UNTRUTH)
            fsetitem(k, e)
    return results


class Untrue(Exception):
    '''Value is untrue.'''
