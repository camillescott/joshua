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

    def build_test_forest(self, n_chroms=10, iv_per_chrom=10, iv_size=10):
        forest = IntervalForest()
        n = 0
        for c in range(n_chroms):
            for i in range(0, iv_per_chrom * iv_size, iv_size):
                f = Interval(i, i + iv_size, idx=n, chrom=str(c))
                forest.add_interval(f)
                n += 1
        return forest
 

    def setUp(self):
        self.forest = self.build_test_forest()

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

    def test_intersect(self):
        other = self.build_test_forest()
        overlaps = self.forest.intersect(other)

        self.assertEquals(len(overlaps), 100)
        for self_idx, other_idx, length in overlaps:
            self.assertEquals(self_idx, other_idx)
            self.assertEquals(length, 10)

if __name__ == "__main__":

    unittest.main()
