# -*- coding: utf-8 -*-
'''test stuf'''

from stuf.six import unittest


class Base(object):

    @property
    def _makeone(self):
        return self._impone(test1='test1', test2='test2', test3=dict(e=1))

    def setUp(self):
        self.stuf = self._makeone

    def test__getattr__(self):
        self.assertEqual(self.stuf.test1, 'test1')
        self.assertEqual(self.stuf.test2, 'test2')
        self.assertEqual(self.stuf.test3.e, 1)

    def test__getitem__(self):
        self.assertEqual(self.stuf['test1'], 'test1')
        self.assertEqual(self.stuf['test2'], 'test2')
        self.assertEqual(self.stuf['test3']['e'], 1)

    def test_get(self):
        self.assertEqual(self.stuf.get('test1'), 'test1')
        self.assertEqual(self.stuf.get('test2'), 'test2')
        self.assertIsNone(self.stuf.get('test4'), 'test4')
        self.assertEqual(self.stuf.get('test3').get('e'), 1)
        self.assertIsNone(self.stuf.get('test3').get('r'))

    def test__setattr__(self):
        self.stuf.max = 3
        self.stuf.test1 = 'test1again'
        self.stuf.test2 = 'test2again'
        self.stuf.test3.e = 5
        self.assertEqual(self.stuf.max, 3)
        self.assertEqual(self.stuf.test1, 'test1again')
        self.assertEqual(self.stuf.test2, 'test2again')
        self.assertEqual(self.stuf.test3.e, 5)

    def test__setitem__(self):
        self.stuf['max'] = 3
        self.stuf['test1'] = 'test1again'
        self.stuf['test2'] = 'test2again'
        self.stuf['test3']['e'] = 5
        self.assertEqual(self.stuf['max'], 3)
        self.assertEqual(self.stuf['test1'], 'test1again')
        self.assertEqual(self.stuf['test2'], 'test2again')
        self.assertEqual(self.stuf['test3']['e'], 5)

    def test__delattr__(self):
        del self.stuf.test1
        del self.stuf.test2
        del self.stuf.test3.e
        self.assertEqual(len(self.stuf.test3), 0)
        del self.stuf.test3
        self.assertRaises(AttributeError, lambda: delattr(self.stuf, 'test4'))
        self.assertEqual(len(self.stuf), 0)
        self.assertRaises(AttributeError, lambda: self.stuf.test1)
        self.assertRaises(AttributeError, lambda: self.stuf.test2)
        self.assertRaises(AttributeError, lambda: self.stuf.test3)
        self.assertRaises(AttributeError, lambda: self.stuf.test3.e)

    def test__delitem__(self):
        del self.stuf['test1']
        del self.stuf['test2']
        del self.stuf['test3']['e']
        self.assertNotIn('e', self.stuf['test3'])
        self.assertTrue(len(self.stuf['test3']) == 0)
        del self.stuf['test3']
        self.assertTrue(len(self.stuf) == 0)
        self.assertNotIn('test1', self.stuf)
        self.assertNotIn('test2', self.stuf)
        self.assertNotIn('test3', self.stuf)

    def test__cmp__(self):
        tstuff = self._makeone
        self.assertEqual(self.stuf, tstuff)

    def test__len__(self):
        self.assertEqual(len(self.stuf), 3)
        self.assertEqual(len(self.stuf.test3), 1)

    def test_repr(self):
        from stuf.six import strings
        self.assertIsInstance(repr(self._makeone), strings)
        self.assertIsInstance(repr(self.stuf), strings)

    def test_items(self):
        slist = list(self.stuf.items())
        self.assertIn(('test1', 'test1'), slist)
        self.assertIn(('test2', 'test2'), slist)
        self.assertIn(('test3', {'e': 1}), slist)

    def test_iteritems(self):
        slist = list(self.stuf.iteritems())
        self.assertIn(('test1', 'test1'), slist)
        self.assertIn(('test2', 'test2'), slist)
        self.assertIn(('test3', {'e': 1}), slist)

    def test_iter(self):
        slist = list(self.stuf)
        slist2 = list(self.stuf.test3)
        self.assertIn('test1', slist)
        self.assertIn('test2', slist)
        self.assertIn('test3', slist)
        self.assertIn('e', slist2)

    def test_iterkeys(self):
        slist = list(self.stuf.iterkeys())
        slist2 = list(self.stuf.test3.iterkeys())
        self.assertIn('test1', slist)
        self.assertIn('test2', slist)
        self.assertIn('test3', slist)
        self.assertIn('e', slist2)

    def test_itervalues(self):
        slist = list(self.stuf.itervalues())
        slist2 = list(self.stuf.test3.itervalues())
        self.assertIn('test1', slist)
        self.assertIn('test2', slist)
        self.assertIn({'e': 1}, slist)
        self.assertIn(1, slist2)

    def test_values(self):
        slist1 = self.stuf.test3.values()
        slist2 = self.stuf.values()
        self.assertIn(1, slist1)
        self.assertIn('test1', slist2)
        self.assertIn('test2', slist2)
        self.assertIn({'e': 1}, slist2)

    def test_keys(self):
        slist1 = self.stuf.test3.keys()
        slist2 = self.stuf.keys()
        self.assertIn('e', slist1)
        self.assertIn('test1', slist2)
        self.assertIn('test2', slist2)
        self.assertIn('test3', slist2)

    def test_pickle(self):
        import pickle
        tstuf = self._makeone
        pkle = pickle.dumps(tstuf)
        nstuf = pickle.loads(pkle)
        self.assertIsInstance(nstuf, self._impone)
        self.assertEqual(tstuf, nstuf)

    def test_clear(self):
        self.stuf.test3.clear()
        self.assertEqual(len(self.stuf.test3), 0)
        self.stuf.clear()
        self.assertEqual(len(self.stuf), 0)

    def test_pop(self):
        self.assertEqual(self.stuf.test3.pop('e'), 1)
        self.assertEqual(self.stuf.pop('test1'), 'test1')
        self.assertEqual(self.stuf.pop('test2'), 'test2')
        self.assertEqual(self.stuf.pop('test3'), {})

    def test_copy(self):
        tstuf = self._makeone
        nstuf = tstuf.copy()
        self.assertIsInstance(nstuf, self._impone)
        self.assertIsInstance(tstuf, self._impone)
        self.assertEqual(tstuf, nstuf)

    def test_popitem(self):
        item = self.stuf.popitem()
        self.assertEqual(len(item) + len(self.stuf), 4, item)

    def test_setdefault(self):
        self.assertEqual(self.stuf.test3.setdefault('e', 8), 1)
        self.assertEqual(self.stuf.test3.setdefault('r', 8), 8)
        self.assertEqual(self.stuf.setdefault('test1', 8), 'test1')
        self.assertEqual(self.stuf.setdefault('pow', 8), 8)

    def test_update(self):
        tstuff = self._makeone
        tstuff['test1'] = 3
        tstuff['test2'] = 6
        tstuff['test3'] = dict(f=2)
        self.stuf.update(tstuff)
        self.assertEqual(self.stuf['test1'], 3, self.stuf.items())
        self.assertEqual(self.stuf['test2'], 6)
        self.assertEqual(self.stuf['test3'], dict(f=2), self.stuf)

    def test_nofile(self):
        import sys
        s = self._impone(a=sys.stdout, b=1)
        self.assertEqual(s.a, sys.stdout)
        t = self._impone(a=[sys.stdout], b=1)
        self.assertEqual(t.a, [sys.stdout])


class TestStuf(Base, unittest.TestCase):

    @property
    def _impone(self):
        from stuf import stuf
        return stuf


class TestDefaultStuf(Base, unittest.TestCase):

    @property
    def _impone(self):
        from stuf import defaultstuf
        return defaultstuf

    @property
    def _makeone(self):
        return self._impone(
            list, test1='test1', test2='test2', test3=dict(e=1)
        )

    def test__getattr__(self):
        self.assertEqual(self.stuf.test1, 'test1')
        self.assertEqual(self.stuf.test2, 'test2')
        self.assertEqual(self.stuf.test4, [])
        self.assertEqual(self.stuf.test3.e, 1)
        self.assertEqual(self.stuf.test3.f, [])

    def test__getitem__(self):
        self.assertEqual(self.stuf['test1'], 'test1')
        self.assertEqual(self.stuf['test2'], 'test2')
        self.assertEqual(self.stuf['test4'], [])
        self.assertEqual(self.stuf['test3']['e'], 1)
        self.assertEqual(self.stuf['test3']['f'], [])

    def test__delattr__(self):
        del self.stuf.test1
        del self.stuf.test2
        del self.stuf.test3.e
        self.assertEqual(len(self.stuf.test3), 0)
        del self.stuf.test3
        self.assertEqual(len(self.stuf), 0)
        self.assertEqual(self.stuf.test1, [])
        self.assertEqual(self.stuf.test2, [])
        self.assertEqual(self.stuf.test3, [])
        self.assertRaises(AttributeError, lambda: self.stuf.test3.e)

    def test__delitem__(self):
        del self.stuf['test1']
        del self.stuf['test2']
        del self.stuf['test3']['e']
        self.assertNotIn('e', self.stuf['test3'])
        self.assertEqual(len(self.stuf['test3']), 0)
        self.assertEqual(self.stuf['test3']['e'], [])
        del self.stuf['test3']
        self.assertEqual(len(self.stuf), 0)
        self.assertNotIn('test1', self.stuf)
        self.assertNotIn('test2', self.stuf)
        self.assertNotIn('test3', self.stuf)
        self.assertEqual(self.stuf['test1'], [])
        self.assertEqual(self.stuf['test2'], [])
        self.assertEqual(self.stuf['test3'], [])
        self.assertRaises(TypeError, lambda: self.stuf['test3']['e'])

    def test_clear(self):
        self.stuf.test3.clear()
        self.assertEqual(len(self.stuf.test3), 0)
        self.assertEqual(self.stuf['test3']['e'], [])
        self.stuf.clear()
        self.assertEqual(len(self.stuf), 0)
        self.assertEqual(self.stuf['test1'], [])
        self.assertEqual(self.stuf['test2'], [])
        self.assertEqual(self.stuf['test3'], [])

    def test_nofile(self):
        import sys
        s = self._impone(list, a=sys.stdout, b=1)
        self.assertEqual(s.a, sys.stdout)
        t = self._impone(list, a=[sys.stdout], b=1)
        self.assertEqual(t.a, [sys.stdout])


class TestFixedStuf(Base, unittest.TestCase):

    @property
    def _impone(self):
        from stuf import fixedstuf
        return fixedstuf

    def test__setattr__(self):
        self.assertRaises(AttributeError, lambda: setattr(self.stuf, 'max', 3))
        self.stuf.test1 = 'test1again'
        self.stuf.test2 = 'test2again'
        self.stuf.test3.e = 5
        self.assertRaises(AttributeError, lambda: self.stuf.max)
        self.assertEqual(self.stuf.test1, 'test1again')
        self.assertEqual(self.stuf.test2, 'test2again')
        self.assertEqual(self.stuf.test3.e, 5)

    def test__setitem__(self):
        self.assertRaises(KeyError, lambda: self.stuf.__setitem__('max', 3))
        self.stuf['test1'] = 'test1again'
        self.stuf['test2'] = 'test2again'
        self.stuf['test3']['e'] = 5
        self.assertRaises(KeyError, lambda: self.stuf.__getitem__('max'))
        self.assertEqual(self.stuf['test1'], 'test1again')
        self.assertEqual(self.stuf['test2'], 'test2again')
        self.assertEqual(self.stuf['test3']['e'], 5)

    def test__delattr__(self):
        self.assertRaises(TypeError, lambda: delattr(self.stuf.test1))
        self.assertRaises(TypeError, lambda: delattr(self.stuf.test3.e))

    def test__delitem__(self):
        del self.stuf.test3['e']
        self.assertRaises(KeyError, lambda: self.stuf.test3['e'])
        del self.stuf['test1']
        self.assertRaises(KeyError, lambda: self.stuf['test1'])

    def test_clear(self):
        self.assertRaises(KeyError, lambda: self.stuf.__setitem__('max', 3))
        self.stuf.clear()
        self.stuf['test1'] = 'test1again'
        self.stuf['test3'] = 5

    def test_pop(self):
        self.assertRaises(AttributeError, lambda: self.stuf.test3.pop('e'))
        self.assertRaises(AttributeError, lambda: self.stuf.pop('test1'))

    def test_popitem(self):
        self.assertRaises(AttributeError, lambda: self.stuf.test3.popitem())
        self.assertRaises(AttributeError, lambda: self.stuf.popitem())

    def test_setdefault(self):
        self.assertEqual(self.stuf.test3.setdefault('e', 8), 1)
        self.assertRaises(KeyError, lambda: self.stuf.test3.setdefault('r', 8))
        self.assertEqual(self.stuf.setdefault('test1', 8), 'test1')
        self.assertRaises(KeyError, lambda: self.stuf.setdefault('pow', 8))


class TestFrozenStuf(Base, unittest.TestCase):

    @property
    def _impone(self):
        from stuf import frozenstuf
        return frozenstuf

    def test__setattr__(self):
        self.assertRaises(AttributeError, setattr(self.stuf, 'max', 3))
        self.assertRaises(
            AttributeError, setattr(self.stuf, 'test1', 'test1again')
        )
        self.assertRaises(
            AttributeError, setattr(self.stuf.test3, 'e', 5)
        )

    def test__setitem__(self):
        self.assertRaises(
            AttributeError, lambda: self.stuf.__setitem__('max', 3)
        )
        self.assertRaises(
            AttributeError,
            lambda: self.stuf.__setitem__('test2', 'test2again'),
        )
        self.assertRaises(
            AttributeError, lambda: self.stuf.test3.__setitem__('e', 5)
        )

    def test__delattr__(self):
        self.assertRaises(TypeError, lambda: delattr(self.stuf.test1))
        self.assertRaises(TypeError, lambda: delattr(self.stuf.test3.e))

    def test__delitem__(self):
        self.assertRaises(
            AttributeError, lambda: self.stuf.__delitem__('test1'),
        )
        self.assertRaises(
            AttributeError, lambda: self.stuf.test3.__delitem__('test1'),
        )

    def test_clear(self):
        self.assertRaises(AttributeError, lambda: self.stuf.test3.clear())
        self.assertRaises(AttributeError, lambda: self.stuf.clear())

    def test_pop(self):
        self.assertRaises(AttributeError, lambda: self.stuf.test3.pop('e'))
        self.assertRaises(AttributeError, lambda: self.stuf.pop('test1'))

    def test_popitem(self):
        self.assertRaises(AttributeError, lambda: self.stuf.test3.popitem())
        self.assertRaises(AttributeError, lambda: self.stuf.popitem())

    def test_setdefault(self):
        self.assertRaises(
            AttributeError, lambda: self.stuf.test3.setdefault('e', 8)
        )
        self.assertRaises(
            AttributeError, lambda: self.stuf.test3.setdefault('r', 8)
        )
        self.assertRaises(
            AttributeError, lambda: self.stuf.setdefault('test1', 8)
        )
        self.assertRaises(
            AttributeError, lambda: self.stuf.setdefault('pow', 8)
        )

    def test_update(self):
        tstuff = self._makeone
        self.assertRaises(
            AttributeError, lambda: self.stuf.test3.update(tstuff),
        )
        self.assertRaises(AttributeError, lambda: self.stuf.update(tstuff))


class TestOrderedStuf(Base, unittest.TestCase):

    @property
    def _impone(self):
        from stuf import orderedstuf
        return orderedstuf

    def test_reversed(self):
        slist = list(reversed(self.stuf))
        self.assertIn('test1', slist)
        self.assertIn('test2', slist)
        self.assertIn('test3', slist)


class TestChainStuf(Base, unittest.TestCase):

    @property
    def _impone(self):
        from stuf.core import chainstuf
        return chainstuf

    def test_basics(self):
        import copy
        import pickle
        from stuf.six import items
        c = self._impone()
        c.a = 1
        c.b = 2
        d = c.new_child()
        d.b = 20
        d.c = 30
        # check internal state
        self.assertEqual(d.maps, [{'b':20, 'c':30}, {'a':1, 'b':2}])
        # check items/iter/getitem
        self.assertEqual(items(d), items(dict(a=1, b=20, c=30)))
        # check len
        self.assertEqual(len(d), 3)
        # check contains
        for key in 'abc':
            self.assertIn(key, d)
        # check get
        for k, v in items(dict(a=1, b=20, c=30, z=100)):
            self.assertEqual(d.get(k, 100), v)
        # unmask a value
        del d['b']
        # check internal state
        self.assertEqual(d.maps, [{'c':30}, {'a':1, 'b':2}])
        # check items/iter/getitem
        self.assertEqual(items(d), items(dict(a=1, b=2, c=30)))
        # check len
        self.assertEqual(len(d), 3)
        # check contains
        for key in 'abc':
            self.assertIn(key, d)
        # check get
        for k, v in items(dict(a=1, b=2, c=30, z=100)):
            self.assertEqual(d.get(k, 100), v)
        # check repr
        self.assertIn(repr(d), [
                      type(d).__name__ + "({'c': 30}, {'a': 1, 'b': 2})",
                      type(d).__name__ + "({'c': 30}, {'b': 2, 'a': 1})"
                      ])
        # check shallow copies
        for e in d.copy(), copy.copy(d):
            self.assertEqual(d, e)
            self.assertEqual(d.maps, e.maps)
            self.assertIsNot(d, e)
            self.assertIsNot(d.maps[0], e.maps[0])
            for m1, m2 in zip(d.maps[1:], e.maps[1:]):
                self.assertIs(m1, m2)
        # check deep copies
        for e in [
            pickle.loads(pickle.dumps(d)), copy.deepcopy(d), eval(repr(d))
        ]:
            self.assertEqual(d, e)
            self.assertEqual(d.maps, e.maps)
            self.assertIsNot(d, e)
            for m1, m2 in zip(d.maps, e.maps):
                self.assertIsNot(m1, m2, e)

        f = d.new_child()
        f['b'] = 5
        self.assertEqual(f.maps, [{'b': 5}, {'c':30}, {'a':1, 'b':2}])
        # check parents
        self.assertEqual(f.parents.maps, [{'c':30}, {'a':1, 'b':2}])
        # find first in chain
        self.assertEqual(f['b'], 5)
        # look beyond maps[0]
        self.assertEqual(f.parents['b'], 2)

    def test_contructor(self):
        # no-args --> one new dict
        self.assertEqual(self._impone().maps, [{}])
        # 1 arg --> list
        self.assertEqual(self._impone({1: 2}).maps, [{1:2}])

    def test_bool(self):
        self.assertFalse(self._impone())
        self.assertFalse(self._impone({}, {}))
        self.assertTrue(self._impone({1: 2}, {}))
        self.assertTrue(self._impone({}, {1: 2}))

    def test_missing(self):
        from stuf.six import items

        class DefaultChainMap(self._impone):
            def __missing__(self, key):
                return 999
        d = DefaultChainMap(dict(a=1, b=2), dict(b=20, c=30))
        # check __getitem__ w/missing
        for k, v in items(dict(a=1, b=2, c=30, d=999)):
            self.assertEqual(d[k], v)
        # check get() w/ missing
        for k, v in items(dict(a=1, b=2, c=30, d=77)):
            self.assertEqual(d.get(k, 77), v)
        for k, v in items(dict(a=True, b=True, c=True, d=False)):
            self.assertEqual(k in d, v)  # check __contains__ w/missing
        self.assertEqual(d.pop('a', 1001), 1, d)
        # check pop() w/missing
        self.assertEqual(d.pop('a', 1002), 1002)
        # check popitem() w/missing
        self.assertEqual(d.popitem(), ('b', 2))
        with self.assertRaises(KeyError):
            d.popitem()

    def test_dict_coercion(self):
        d = self._impone(dict(a=1, b=2), dict(b=20, c=30))
        self.assertEqual(dict(d), dict(a=1, b=2, c=30))
        self.assertEqual(dict(d.items()), dict(a=1, b=2, c=30))


#class TestCountStuf(Base, unittest.TestCase):
#
#    @property
#    def _impone(self):
#        from stuf.core import countstuf
#        return countstuf
#
#    def test_basics(self):
#        from collections import Mapping
#        c = self._impone('abcaba'.split())
#        self.assertEqual(c, self._impone({'a': 3, 'b': 2, 'c': 1}))
#        self.assertEqual(c, self._impone(a=3, b=2, c=1))
#        self.assertIsInstance(c, dict)
#        self.assertIsInstance(c, Mapping)
#        self.assertTrue(issubclass(self._impone, dict))
#        self.assertTrue(issubclass(self._impone, Mapping))
#        self.assertEqual(len(c), 3)
#        self.assertEqual(sum(c.values()), 6)
#        self.assertEqual(sorted(c.values()), [1, 2, 3])
#        self.assertEqual(sorted(c.keys()), ['a', 'b', 'c'])
#        self.assertEqual(sorted(c), ['a', 'b', 'c'])
#        self.assertEqual(sorted(c.items()), [('a', 3), ('b', 2), ('c', 1)])
#        self.assertEqual(c['b'], 2)
#        self.assertEqual(c['z'], 0)
#        self.assertEqual(c.__contains__('c'), True)
#        self.assertEqual(c.__contains__('z'), False)
#        self.assertEqual(c.get('b', 10), 2)
#        self.assertEqual(c.get('z', 10), 10)
#        self.assertEqual(c, dict(a=3, b=2, c=1))
#        self.assertEqual(repr(c), "countstuf({'a': 3, 'b': 2, 'c': 1})")
#        self.assertEqual(c.most_common(), [('a', 3), ('b', 2), ('c', 1)])
#        for i in range(5):
#            self.assertEqual(
#                c.most_common(i), [('a', 3), ('b', 2), ('c', 1)][:i]
#            )
#        self.assertEqual(''.join(sorted(c.elements())), 'aaabbc')
#        c['a'] += 1         # increment an existing value
#        c['b'] -= 2         # sub existing value to zero
#        del c['c']          # remove an entry
#        del c['c']          # make sure that del doesn't raise KeyError
#        c['d'] -= 2         # sub from a missing value
#        c['e'] = -5         # directly assign a missing value
#        c['f'] += 4         # add to a missing value
#        self.assertEqual(c, dict(a=4, b=0, d=-2, e=-5, f=4))
#        self.assertEqual(''.join(sorted(c.elements())), 'aaaaffff')
#        self.assertEqual(c.pop('f'), 4)
#        self.assertNotIn('f', c)
#        for i in range(3):
#            elem, cnt = c.popitem()
#            self.assertNotIn(elem, c)
#        c.clear()
#        self.assertEqual(c, {})
#        self.assertEqual(repr(c), 'countstuf()')
#        self.assertRaises(NotImplementedError, self._impone.fromkeys, 'abc')
#        self.assertRaises(TypeError, hash, c)
#        c.update(dict(a=5, b=3))
#        c.update(c=1)
#        c.update(self._impone('a' * 50 + 'b' * 30))
#        c.update()          # test case with no args
#        c.__init__('a' * 500 + 'b' * 300)
#        c.__init__('cdc')
#        c.__init__()
#        self.assertEqual(c, dict(a=555, b=333, c=3, d=1))
#        self.assertEqual(c.setdefault('d', 5), 1)
#        self.assertEqual(c['d'], 1)
#        self.assertEqual(c.setdefault('e', 5), 5)
#        self.assertEqual(c['e'], 5)
#
#    def test_copying(self):
#        import copy
#        import pickle
#        # Check that counters are copyable, deepcopyable, picklable, and
#        # have a repr/eval round-trip
#        from stuf.core import countstuf
#        words = self._impone(
#            'which witch had which witches wrist watch'.split()
#        )
#        update_test = self._impone()
#        update_test.update(words)
#        for i, dup in enumerate([
#            words.copy(),
#            copy.copy(words),
#            copy.deepcopy(words),
#            pickle.loads(pickle.dumps(words, 0)),
#            pickle.loads(pickle.dumps(words, 1)),
#            pickle.loads(pickle.dumps(words, 2)),
#            pickle.loads(pickle.dumps(words, -1)),
#            eval(repr(words)),
#            update_test,
#            self._impone(words),
#        ]):
#            msg = (i, dup, words)
#            self.assertTrue(dup is not words)
#            self.assertEqual(dup, words)
#            self.assertEqual(len(dup), len(words))
#            self.assertEqual(type(dup), type(words))
#
#    def test_copy_subclass(self):
#        class MyCounter(self._impone):
#            pass
#        c = MyCounter('slartibartfast')
#        d = c.copy()
#        self.assertEqual(d, c)
#        self.assertEqual(len(d), len(c))
#        self.assertEqual(type(d), type(c))
#
#    def test_conversions(self):
#        # Convert to: set, list, dict
#        s = 'she sells sea shells by the sea shore'.split()
#        self.assertEqual(sorted(self._impone(s).elements()), sorted(s))
#        self.assertEqual(sorted(self._impone(s)), sorted(set(s)))
#        self.assertEqual(dict(self._impone(s)), dict(self._impone(s).items()))
#        self.assertEqual(set(self._impone(s)), set(s))
#
#    def test_invariant_for_the_in_operator(self):
#        c = self._impone(a=10, b=-2, c=0)
#        for elem in c:
#            self.assertTrue(elem in c)
#            self.assertIn(elem, c)
#
#    def test_multiset_operations(self):
#        from random import randrange
#        # Verify that adding a zero counter will strip zeros and negatives
#        c = self._impone(a=10, b=-2, c=0) + self._impone()
#        self.assertEqual(dict(c), dict(a=10))
#        elements = 'abcd'
#        for i in range(1000):
#            # test random pairs of multisets
#            p = self._impone(
#                dict((elem, randrange(-2, 4)) for elem in elements))
#            p.update(e=1, f=-1, g=0)
#            q = self._impone(
#                dict((elem, randrange(-2, 4)) for elem in elements)
#            )
#            q.update(h=1, i=-1, j=0)
#            for counterop, numberop in [
#                (self._impone.__add__, lambda x, y: max(0, x + y)),
#                (self._impone.__sub__, lambda x, y: max(0, x - y)),
#                (self._impone.__or__, lambda x, y: max(0, x, y)),
#                (self._impone.__and__, lambda x, y: max(0, min(x, y))),
#            ]:
#                result = counterop(p, q)
#                for x in elements:
#                    self.assertEqual(
#                        numberop(p[x], q[x]), result[x], (counterop, x, p, q)
#                    )
#                # verify that results exclude non-positive counts
#                self.assertTrue(x > 0 for x in result.values())
#        elements = 'abcdef'
#        for i in range(100):
#            # verify that random multisets with no repeats are exactly like
#            # sets
#            p = self._impone(
#                dict((elem, randrange(0, 2)) for elem in elements))
#            q = self._impone(
#                dict((elem, randrange(0, 2)) for elem in elements))
#            for counterop, setop in [
#                (self._impone.__sub__, set.__sub__),
#                (self._impone.__or__, set.__or__),
#                (self._impone.__and__, set.__and__),
#            ]:
#                counter_result = counterop(p, q)
#                set_result = setop(set(p.elements()), set(q.elements()))
#                self.assertEqual(counter_result, dict.fromkeys(set_result, 1))
#
#    def test_inplace_operations(self):
#        from random import randrange
#        from stuf.core import countstuf
#        elements = 'abcd'
#        for i in range(1000):
#            # test random pairs of multisets
#            p = self._impone(
#                dict((elem, randrange(-2, 4)) for elem in elements)
#            )
#            p.update(e=1, f=-1, g=0)
#            q = self._impone(
#                dict((elem, randrange(-2, 4)) for elem in elements)
#            )
#            q.update(h=1, i=-1, j=0)
#            for inplace_op, regular_op in [
#                (countstuf.__iadd__, countstuf.__add__),
#                (countstuf.__iand__, countstuf.__and__),
#                (countstuf.__ior__, countstuf.__or__),
#                (countstuf.__isub__, countstuf.__sub__),
#            ]:
#                c = p.copy()
#                c_id = id(c)
#                regular_result = regular_op(c, q)
#                inplace_result = inplace_op(c, q)
#                self.assertEqual(inplace_result, regular_result)
#                self.assertEqual(id(inplace_result), c_id)
#
#    def test_subtract(self):
#        c = self._impone(a=-5, b=0, c=5, d=10, e=15, g=40)
#        c.subtract(a=1, b=2, c=-3, d=10, e=20, f=30, h=-50)
#        self.assertEqual(
#            c, self._impone(a=-6, b=-2, c=8, d=0, e=-5, f=-30, g=40, h=50))
#        c = self._impone(a=-5, b=0, c=5, d=10, e=15, g=40)
#        c.subtract(self._impone(a=1, b=2, c=-3, d=10, e=20, f=30, h=-50))
#        self.assertEqual(
#            c, self._impone(a=-6, b=-2, c=8, d=0, e=-5, f=-30, g=40, h=50)
#        )
#        c = self._impone(*'aaabbcd'.split())
#        c.subtract('aaaabbcce')
#        self.assertEqual(c, self._impone(a=-1, b=0, c=-1, d=1, e=-1))
#
#    def test_unary(self):
#        c = self._impone(a=-5, b=0, c=5, d=10, e=15, g=40)
#        self.assertEqual(dict(+c), dict(c=5, d=10, e=15, g=40))
#        self.assertEqual(dict(-c), dict(a=5))
#
#    def test_repr_nonsortable(self):
#        c = self._impone(a=2, b=None)
#        r = repr(c)
#        self.assertIn("('a', 2)", r)
#        self.assertIn("('b', None)", r)


if __name__ == '__main__':
    unittest.main()
