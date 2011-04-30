import unittest


class TestStufDict(unittest.TestCase):

    @property
    def _makeone(self):
        from stuf import stufdict
        return stufdict

    def setUp(self):
        self.stuf = self._makeone()

    def test__getitem__(self):
        self.stuf['max'] = 3
        self.assertEqual(self.stuf['max'], 3)

    def test__setitem__(self):
        self.stuf['max'] = 3
        self.assertEqual(self.stuf['max'], 3)

    def test__delitem__(self):
        self.stuf['max'] = 3
        del self.stuf['max']
        self.assertEqual('max' in self.stuf, False)

    def test_get(self):
        self.stuf['max'] = 3
        self.assertEqual(self.stuf.get('min'), None)

    def test__cmp__(self):
        tstuff = self._makeone()
        self.stuf['max'] = 3
        tstuff['max'] = 3
        self.assertEqual(self.stuf, tstuff)

    def test__len__(self):
        self.stuf['max'] = 3
        self.stuf['min'] = 6
        self.assertEqual(len(self.stuf), 2)

    def test_clear(self):
        self.stuf['max'] = 3
        self.stuf['min'] = 6
        self.stuf['pow'] = 7
        self.stuf.clear()
        self.assertEqual(len(self.stuf), 0)

    def test_items(self):
        self.stuf['max'] = 3
        self.stuf['min'] = 6
        self.stuf['pow'] = 7
        slist = list(self.stuf.items())
        self.assertEqual(('min', 6) in slist, True)

    def test_iteritems(self):
        self.stuf['max'] = 3
        self.stuf['min'] = 6
        self.stuf['pow'] = 7
        slist = list(self.stuf.iteritems())
        self.assertEqual(('min', 6) in slist, True)

    def test_iterkeys(self):
        self.stuf['max'] = 3
        self.stuf['min'] = 6
        self.stuf['pow'] = 7
        slist = list(self.stuf.iterkeys())
        self.assertEqual('min' in slist, True)

    def test_itervalues(self):
        self.stuf['max'] = 3
        self.stuf['min'] = 6
        self.stuf['pow'] = 7
        slist = list(self.stuf.itervalues())
        self.assertEqual(6 in slist, True)

    def test_pop(self):
        self.stuf['max'] = 3
        self.stuf['min'] = 6
        item = self.stuf.pop('min')
        self.assertEqual(item, 6)

    def test_popitem(self):
        self.stuf['max'] = 3
        self.stuf['min'] = 6
        self.stuf['pow'] = 7
        item = self.stuf.popitem()
        self.assertEqual(len(item) + len(self.stuf), 4)

    def test_setdefault(self):
        self.stuf['max'] = 3
        self.stuf['min'] = 6
        self.stuf['powl'] = 7
        self.stuf.setdefault('pow', 8)
        self.assertEqual(self.stuf['pow'], 8)

    def test_update(self):
        tstuff = self._makeone()
        tstuff['max'] = 3
        tstuff['min'] = 6
        tstuff['pow'] = 7
        self.stuf['max'] = 2
        self.stuf['min'] = 3
        self.stuf['pow'] = 7
        self.stuf.update(tstuff)
        self.assertEqual(self.stuf['min'], 6)

    def test_values(self):
        self.stuf['max'] = 3
        self.stuf['min'] = 6
        self.stuf['pow'] = 7
        slist = self.stuf.values()
        self.assertEqual(6 in slist, True)

    def test_keys(self):
        self.stuf['max'] = 3
        self.stuf['min'] = 6
        self.stuf['pow'] = 7
        slist = self.stuf.keys()
        self.assertEqual('min' in slist, True)




class TestStuf(unittest.TestCase):

    @property
    def _makeone(self):
        from stuf import stuf
        return stuf

    def setUp(self):
        self.stuf = self._makeone(test1='test1', test2='test2')

    def test__getattr__(self):
        self.assertEqual(self.stuf.test1, 'test1')
        self.assertEqual(self.stuf.test2, 'test2')

    def test__getitem__(self):
        self.assertEqual(self.stuf['test1'], 'test1')
        self.assertEqual(self.stuf['test2'], 'test2')

    def test__setattr__(self):
        self.stuf.max = 3
        self.stuf.test1 = 'test1again'
        self.stuf.test2 = 'test2again'
        self.assertEqual(self.stuf.max, 3)
        self.assertEqual(self.stuf.test1, 'test1again')
        self.assertEqual(self.stuf.test2, 'test2again')

    def test__setitem__(self):
        self.stuf['max'] = 3
        self.stuf['test1'] = 'test1again'
        self.stuf['test2'] = 'test2again'
        self.assertEqual(self.stuf['max'], 3)
        self.assertEqual(self.stuf['test1'], 'test1again')
        self.assertEqual(self.stuf['test2'], 'test2again')

    def test__delattr__(self):
        del self.stuf.test1
        del self.stuf.test2
        self.assertTrue(len(self.stuf)==0)
        self.assertRaises(AttributeError, lambda: self.stuf.test1)
        self.assertRaises(AttributeError, lambda: self.stuf.test2)

    def test__delitem__(self):
        del self.stuf['test1']
        del self.stuf['test2']
        self.assertTrue(len(self.stuf)==0)
        self.assertFalse('test1' in self.stuf)
        self.assertFalse('test2' in self.stuf)

    def test_get(self):
        self.assertEqual(self.stuf.get('test1'), 'test1')
        self.assertEqual(self.stuf.get('test2'), 'test2')
        self.assertIsNone(self.stuf.get('test3'))

    def test__cmp__(self):
        tstuff = self._makeone(test1='test1', test2='test2')
        self.assertEqual(self.stuf, tstuff)

    def test__len__(self):
        self.assertEqual(len(self.stuf), 2)

    def test_clear(self):
        self.stuf.clear()
        self.assertEqual(len(self.stuf), 0)

    def test_items(self):
        slist = list(self.stuf.items())
        self.assertEqual(('test1', 'test1') in slist, True)

    def test_iteritems(self):
        slist = list(self.stuf.iteritems())
        self.assertEqual(('test1', 'test1') in slist, True)

    def test_iterkeys(self):
        slist = list(self.stuf.iterkeys())
        self.assertEqual('test1' in slist, True)

    def test_itervalues(self):
        slist = list(self.stuf.itervalues())
        self.assertEqual('test1' in slist, True)

    def test_pop(self):
        item = self.stuf.pop('test1')
        self.assertEqual(item, 'test1')

    def test_popitem(self):
        item = self.stuf.popitem()
        self.assertEqual(len(item) + len(self.stuf), 3)

    def test_setdefault(self):
        self.assertEqual(self.stuf.setdefault('test1', 8), 'test1')
        self.assertEqual(self.stuf.setdefault('pow', 8), 8)

    def test_update(self):
        tstuff = self._makeone(test1='test1', test2='test2')
        tstuff['test1'] = 3
        tstuff['test2'] = 6
        self.stuf.update(tstuff)
        self.assertEqual(self.stuf['test1'], 3)
        self.assertEqual(self.stuf['test2'], 6)

    def test_values(self):
        slist = self.stuf.values()
        self.assertEqual('test1' in slist, True)
        self.assertEqual('test2' in slist, True)

    def test_keys(self):
        slist = self.stuf.keys()
        self.assertEqual('test1' in slist, True)
        self.assertEqual('test2' in slist, True)


class TestFrozenStuf(unittest.TestCase):

    @property
    def _makeone(self):
        from stuf import frozenstuf
        return frozenstuf

    def setUp(self):
        self.stuf = self._makeone(test1='test1', test2='test2')

    def test__getattr__(self):
        self.assertEqual(self.stuf.test1, 'test1')
        self.assertEqual(self.stuf.test2, 'test2')

    def test__getitem__(self):
        self.assertEqual(self.stuf['test1'], 'test1')
        self.assertEqual(self.stuf['test2'], 'test2')

    def test__setattr__(self):
        self.assertRaises(AttributeError, lambda: setattr(self.stuf, 'max', 3))
        self.assertRaises(AttributeError, lambda: setattr(self.stuf, 'test1', 3))
        self.assertRaises(AttributeError, lambda: setattr(self.stuf, 'test1', 3))

    def test__setitem__(self):
        self.assertRaises(AttributeError, lambda: self.stuf.__setitem__('max', 3))
        self.assertRaises(AttributeError, lambda: self.stuf.__setitem__('test1', 3))
        self.assertRaises(AttributeError, lambda: self.stuf.__setitem__('test1', 3))

    def test__delattr__(self):
        self.assertRaises(AttributeError, lambda: delattr(self.stuf, 'test1'))
        self.assertRaises(AttributeError, lambda: delattr(self.stuf, 'test2'))
        self.assertTrue(len(self.stuf)==2)

    def test__delitem__(self):
        self.assertRaises(AttributeError, lambda: self.stuf.__delitem__('test1'))
        self.assertRaises(AttributeError, lambda: self.stuf.__delitem__('test2'))
        self.assertTrue(len(self.stuf)==2)

    def test_get(self):
        self.assertEqual(self.stuf.get('test1'), 'test1')
        self.assertEqual(self.stuf.get('test2'), 'test2')
        self.assertIsNone(self.stuf.get('test3'))

    def test__cmp__(self):
        tstuff = self._makeone(test1='test1', test2='test2')
        self.assertEqual(self.stuf, tstuff)

    def test__len__(self):
        self.assertEqual(len(self.stuf), 2)

    def test_clear(self):
        self.assertRaises(AttributeError, lambda: self.stuf.clear())

    def test_items(self):
        slist = list(self.stuf.items())
        self.assertEqual(('test1', 'test1') in slist, True)

    def test_iteritems(self):
        slist = list(self.stuf.iteritems())
        self.assertEqual(('test1', 'test1') in slist, True)

    def test_iterkeys(self):
        slist = list(self.stuf.iterkeys())
        self.assertEqual('test1' in slist, True)

    def test_itervalues(self):
        slist = list(self.stuf.itervalues())
        self.assertEqual('test1' in slist, True)

    def test_pop(self):
        self.assertEqual(self.stuf.pop, dict.pop, self.stuf.pop)
        self.assertRaises(AttributeError, lambda: self.stuf.pop('test1', None))

    def test_popitem(self):
        self.assertRaises(AttributeError, lambda: self.stuf.popitem())

    def test_setdefault(self):
        self.assertRaises(AttributeError, lambda: self.stuf.setdefault('test1', 8))

    def test_update(self):
        tstuf = self._makeone(test1='test1', test2='test2')
        self.assertRaises(AttributeError, lambda: self.stuf.update(tstuf))

    def test_values(self):
        slist = self.stuf.values()
        self.assertEqual('test1' in slist, True)
        self.assertEqual('test2' in slist, True)

    def test_keys(self):
        slist = self.stuf.keys()
        self.assertEqual('test1' in slist, True)
        self.assertEqual('test2' in slist, True)


if __name__ == '__main__':
    unittest.main()
