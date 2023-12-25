def merge_sort(arr):
    if len(arr) <= 1:
        return 0, 0

    mid = len(arr) // 2
    L = arr[:mid]
    R = arr[mid:]

    accesses_left, comparisons_left = merge_sort(L)
    accesses_right, comparisons_right = merge_sort(R)
    accesses_merge, comparisons_merge = merge(arr, L, R)

    total_accesses = accesses_left + accesses_right + accesses_merge
    total_comparisons = comparisons_left + comparisons_right + comparisons_merge

    return total_accesses, total_comparisons


def merge(arr, L, R):
    i = j = k = 0
    accesses = 0
    comparisons = 0

    while i < len(L) and j < len(R):
        comparisons += 1
        if L[i] < R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
        accesses += 3

    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1
        accesses += 2

    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1
        accesses += 2

    return accesses, comparisons
