import unittest


class TestStuffDict(unittest.TestCase):

    @property
    def _makeone(self):
        from stuff import stuffdict
        return stuffdict

    def setUp(self):
        self.stuff = self._makeone()

    def test__getitem__(self):
        self.stuff['max'] = 3
        self.assertEqual(self.stuff['max'], 3)

    def test__setitem__(self):
        self.stuff['max'] = 3
        self.assertEqual(self.stuff['max'], 3)

    def test__delitem__(self):
        self.stuff['max'] = 3
        del self.stuff['max']
        self.assertEqual('max' in self.stuff, False)

    def test_get(self):
        self.stuff['max'] = 3
        self.assertEqual(self.stuff.get('min'), None)

    def test__cmp__(self):
        tstuff = self._makeone()
        self.stuff['max'] = 3
        tstuff['max'] = 3
        self.assertEqual(self.stuff, tstuff)

    def test__len__(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.assertEqual(len(self.stuff), 2)

    def test_clear(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        self.stuff.clear()
        self.assertEqual(len(self.stuff), 0)

    def test_items(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        slist = list(self.stuff.items())
        self.assertEqual(('min', 6) in slist, True)

    def test_iteritems(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        slist = list(self.stuff.iteritems())
        self.assertEqual(('min', 6) in slist, True)

    def test_iterkeys(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        slist = list(self.stuff.iterkeys())
        self.assertEqual('min' in slist, True)

    def test_itervalues(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        slist = list(self.stuff.itervalues())
        self.assertEqual(6 in slist, True)

    def test_pop(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        item = self.stuff.pop('min')
        self.assertEqual(item, 6)

    def test_popitem(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        item = self.stuff.popitem()
        self.assertEqual(len(item) + len(self.stuff), 4)

    def test_setdefault(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['powl'] = 7
        self.stuff.setdefault('pow', 8)
        self.assertEqual(self.stuff['pow'], 8)

    def test_update(self):
        tstuff = self._makeone()
        tstuff['max'] = 3
        tstuff['min'] = 6
        tstuff['pow'] = 7
        self.stuff['max'] = 2
        self.stuff['min'] = 3
        self.stuff['pow'] = 7
        self.stuff.update(tstuff)
        self.assertEqual(self.stuff['min'], 6)

    def test_values(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        slist = self.stuff.values()
        self.assertEqual(6 in slist, True)

    def test_keys(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        slist = self.stuff.keys()
        self.assertEqual('min' in slist, True)


class TestOrderedStuffDict(unittest.TestCase):

    @property
    def _makeone(self):
        from stuff import stuffdict
        return stuffdict

    def setUp(self):
        self.stuff = self._makeone(order=True)

    def test__getitem__(self):
        self.stuff['max'] = 3
        self.assertEqual(self.stuff['max'], 3)

    def test__setitem__(self):
        self.stuff['max'] = 3
        self.assertEqual(self.stuff['max'], 3)

    def test__delitem__(self):
        self.stuff['max'] = 3
        del self.stuff['max']
        self.assertEqual('max' in self.stuff, False)

    def test_get(self):
        self.stuff['max'] = 3
        self.assertEqual(self.stuff.get('min'), None)

    def test__cmp__(self):
        tstuff = self._makeone(order=True)
        self.stuff['max'] = 3
        tstuff['max'] = 3
        self.assertEqual(self.stuff, tstuff)

    def test__len__(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.assertEqual(len(self.stuff), 2)

    def test_clear(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        self.stuff.clear()
        self.assertEqual(len(self.stuff), 0)

    def test_items(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        slist = list(self.stuff.items())
        self.assertEqual(('min', 6) in slist, True)

    def test_iteritems(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        slist = list(self.stuff.iteritems())
        self.assertEqual(('min', 6) in slist, True)

    def test_iterkeys(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        slist = list(self.stuff.iterkeys())
        self.assertEqual('min' in slist, True)

    def test_itervalues(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        slist = list(self.stuff.itervalues())
        self.assertEqual(6 in slist, True)

    def test_pop(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        item = self.stuff.pop('min')
        self.assertEqual(item, 6)

    def test_popitem(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        item = self.stuff.popitem()
        self.assertEqual(len(item) + len(self.stuff), 4)

    def test_setdefault(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['powl'] = 7
        self.stuff.setdefault('pow', 8)
        self.assertEqual(self.stuff['pow'], 8)

    def test_update(self):
        tstuff = self._makeone(order=True)
        tstuff['max'] = 3
        tstuff['min'] = 6
        tstuff['pow'] = 7
        self.stuff['max'] = 2
        self.stuff['min'] = 3
        self.stuff['pow'] = 7
        self.stuff.update(tstuff)
        self.assertEqual(self.stuff['min'], 6)

    def test_values(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        slist = self.stuff.values()
        self.assertEqual(6 in slist, True)

    def test_keys(self):
        self.stuff['max'] = 3
        self.stuff['min'] = 6
        self.stuff['pow'] = 7
        slist = self.stuff.keys()
        self.assertEqual('min' in slist, True)


if __name__ == '__main__':
    unittest.main()
