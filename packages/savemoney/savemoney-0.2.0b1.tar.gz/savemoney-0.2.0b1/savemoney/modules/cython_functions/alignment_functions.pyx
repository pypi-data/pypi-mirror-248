# ビルド
# python rpd_calc_setup.py build_ext --inplace

cimport cython
# import numpy as np
cimport numpy as cnp
# DTYPEint64 = np.int64
ctypedef cnp.int64_t DTYPEint64_t

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
@cython.nonecheck(False)
cpdef k_mer_offset_analysis(
        cnp.ndarray[DTYPEint64_t, ndim=1] ref_seq_v_repeated, 
        cnp.ndarray[DTYPEint64_t, ndim=1] query_seq_v, 
        cnp.ndarray[DTYPEint64_t, ndim=1] result_array, 
    ):
    cdef int k
    cdef int i
    cdef int s
    cdef int len_query
    s = 0
    for k in range(len(result_array)):    # k はオフセット
        for i in range(len(query_seq_v)):
            if ref_seq_v_repeated[k + i] == query_seq_v[i]:
                s += 1
        result_array[k] = s
        s = 0


# from cython.view cimport array
# @cython.boundscheck(False) # turn off bounds-checking for entire function
# @cython.wraparound(False)  # turn off negative index wrapping for entire function
# @cython.nonecheck(False)
# cpdef k_mer_offset_analysis(
#         cnp.ndarray[DTYPEint64_t, ndim=1] ref_seq_v_repeated, 
#         cnp.ndarray[DTYPEint64_t, ndim=1] query_seq_v, 
#         cnp.ndarray[DTYPEint64_t, ndim=1] result_array, 
#     ):
#     cdef long [:] ref_seq_v_repeated_view = ref_seq_v_repeated
#     cdef long [:] query_seq_v_view = query_seq_v
#     cdef long [:] result_array_view = result_array

#     cdef int k
#     cdef int i
#     cdef int s
#     s = 0
#     for k in range(len(result_array_view)):    # k はオフセット
#         for i in range(len(query_seq_v_view)):
#             if ref_seq_v_repeated_view[k + i] == query_seq_v_view[i]:
#                 s += 1
#         result_array_view[k] = s
#         s = 0



