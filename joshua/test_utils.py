#!/usr/bin/env python

import sys, os
import unittest
try:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
except:
    sys.path.insert(0, os.path.dirname(os.path.abspath(".")))

from intervaltree import Interval
from intervaltree import IntervalTree
from intervalforest import IntervalForest

from utils import calc_bases_overlapped_mult
from utils import calc_bases_overlapped_single

class TestCalcBasesOverlappedMult(unittest.TestCase):

    def setUp(self):
        self.test_fn = calc_bases_overlapped_mult
        self.base_iv = Interval(50, 150)

    def test_right_overlap(self):

        iv_roverlap = [Interval(100, 200)]
        self.assertEquals(self.test_fn(self.base_iv, iv_roverlap), 50)

    def test_left_overlap(self):

        iv_loverlap = [Interval(0, 100)]
        self.assertEqual(self.test_fn(self.base_iv, iv_loverlap), 50)

    def test_left_overlap_mult(self):
        iv_left_mult = [Interval(100,200), Interval(200,300)]
        self.assertEquals(self.test_fn(self.base_iv, iv_left_mult), 50)

    def test_contained_overlap(self):
        iv_contained = [Interval(75,125)]
        self.assertEquals(self.test_fn(self.base_iv, iv_contained), 50)

    def test_contains_overlap(self):
        iv_contains = [Interval(0, 200)]
        self.assertEquals(self.test_fn(self.base_iv, iv_contains), 100)

    def test_merged_contains_overlap(self):
        iv_overlap = [Interval(50, 200), Interval(0, 100)]
        self.assertEquals(self.test_fn(self.base_iv, iv_overlap), 100)

    def test_merged_contained_overlap(self):
        iv_overlap = [Interval(50, 75), Interval(70, 100)]
        self.assertEquals(self.test_fn(self.base_iv, iv_overlap), 50)

class TestCalcbasesOverlappedSingle(unittest.TestCase):

    def setUp(self):
        self.test_fn = calc_bases_overlapped_single
        self.start = 50
        self.end = 100

    def test_left_overlap(self):
        self.assertEquals(self.test_fn(self.start, self.end, 0, 75), 25)

    def test_right_overlap(self):
        self.assertEquals(self.test_fn(self.start, self.end, 75, 125), 25)

    def test_contained(self):
        self.assertEquals(self.test_fn(self.start, self.end, 55, 60), 5)

    def test_contains(self):
        self.assertEquals(self.test_fn(self.start, self.end, 0, 125), 50)

if __name__ == "__main__":

    unittest.main()
