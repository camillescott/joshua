import sys, os
import unittest
try:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
except:
    sys.path.insert(0, os.path.dirname(os.path.abspath(".")))

from intervaltree import Interval
from intervaltree import IntervalNode
from intervaltree import IntervalTree
from intervalforest import IntervalForest


class IntervalForestFunctions(unittest.TestCase):

    def setUp(self):
        forest = IntervalForest()
        for c in range(10):
            for i in range(0, 100, 10):
                f = Interval(i, i + 10, chrom=str(c))
                forest.add_interval(f)
        self.forest = forest

    def test_len(self):
        self.assertTrue(len(self.forest) == 100)

    def test_getitem(self):
        tree = self.forest['0']
        def test_fn(node):
            self.assertEquals(node.interval.chrom, '0')
        tree.traverse(test_fn)

    def test_getitem_error(self):
        with self.assertRaises(KeyError):
            tree = self.forest['11']

    def test_contains(self):
        for i in range(10):
            self.assertTrue(str(i) in self.forest)
        self.assertFalse('11' in self.forest)

    def test_add_tree(self):
        self.forest.add_tree('15', IntervalTree())
        self.assertEquals(len(self.forest), 100)
        self.assertEquals(len(self.forest['15']), 0)

if __name__ == "__main__":

    unittest.main()
