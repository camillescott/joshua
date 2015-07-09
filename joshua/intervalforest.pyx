import sys, os

from intervaltree import Interval
from intervaltree import IntervalTree

cdef class IntervalForest:

    cdef public dict trees
    cdef public int size

    def __init__(self):
        self.trees = {}
        self.size = 0

    cpdef add_interval(self, object iv):
        key = iv.chrom
        if key not in self:
            self.trees[key] = IntervalTree()
        self.trees[key].add_interval(iv)
        self.size += 1

    cpdef add_tree(self, str key, object tree):
        self.trees[key] = tree
        self.size += len(tree)

    def __contains__(self, str key):
        if key in self.trees:
            return True
        return False

    def __getitem__(self, key):
        return self.trees[key]

    def __len__(self):
        return self.size

    def intersect(self, object other, float cutoff=0.9):

        if type(other) is not IntervalTree:
            raise TypeError('Expected IntervalTree, go {t}'.format(
                            t=type(other)))
        
        cdef list overlaps = []
        
