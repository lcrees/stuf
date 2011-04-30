import unittest


class TestStufDict(unittest.TestCase):

    @property
    def _makeone(self):
        from stuf import stuffdict
        return stuffdict

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


class TestOrderedStuffDict(unittest.TestCase):

    @property
    def _makeone(self):
        from stuf import stuffdict
        return stuffdict

    def setUp(self):
        self.stuf = self._makeone(order=True)

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
        tstuff = self._makeone(order=True)
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
        tstuff = self._makeone(order=True)
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


if __name__ == '__main__':
    unittest.main()
