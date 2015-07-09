'''
Utility code
'''

from intervaltree import IntervalNode, IntervalTree

#cython cdivision=True

cpdef merge_overlapping_sorted(list iv_list):

    if len(iv_list) == 1:
        return iv_list

    cdef object top
    cdef list merge_stack = [iv_list[0]]
    for iv in iv_list[1:]:
        top = merge_stack[-1]
        if top.end < iv.start:
            merge_stack.append(iv)
        elif top.end < iv.end:
            top.end = iv.end
            merge_stack.pop()
            merge_stack.append(top)

    return merge_stack


def merge_overlapping(list iv_list):
    '''
    Merge all overlapping Intervals from the given list, and return a new list
    with the collapsed Intervals
    '''
    if len(iv_list) == 1:
        return iv_list

    def sort_fn(item):
        return item.start

    iv_list = sorted(iv_list, key=sort_fn)

    return merge_overlapping_sorted(iv_list)

cpdef calc_bases_overlapped_mult(object iv, list overlap_ivs):
    '''
    Given a target Interval and a list of *overlapping* Intervals,
    calculate how many bases in the target are overlapped
    '''
    merged = merge_overlapping(overlap_ivs)

    cdef int start = iv.start
    cdef int end = iv.end
    cdef int iv_length = len(iv)

    cdef int covered = 0
    for overlap_iv in merged:
        covered += calc_bases_overlapped_single(start, end, overlap_iv.start, overlap_iv.end)
        if covered >= iv_length:
            covered = iv_length
            break

    return covered

cpdef calc_bases_overlapped_single(int start_a, int end_a, int start_b, int end_b):
    '''
    Given two Intervals, calculate their overlap
    '''

    if start_b <= start_a:
        if end_b <= end_a:
            return end_b - start_a
        else:
            return end_a - start_a
    else:
        if end_b <= end_a:
            return end_b - start_b
        else:
            return end_a - start_b
