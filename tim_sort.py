def insertion_sort(arr, left, right, accesses, comparisons):
    for i in range(left + 1, right + 1):
        temp = arr[i]
        accesses += 1
        j = i - 1
        while j >= left:
            comparisons += 1
            accesses += 1
            if arr[j] > temp:
                arr[j + 1] = arr[j]
                accesses += 2
                j -= 1
            else:
                break
        arr[j + 1] = temp
        accesses += 1
    return accesses, comparisons


def merge(arr, l, m, r, accesses, comparisons):
    len1, len2 = m - l + 1, r - m
    left, right = [], []
    for i in range(len1):
        left.append(arr[l + i])
        accesses += 1
    for i in range(len2):
        right.append(arr[m + 1 + i])
        accesses += 1

    i, j, k = 0, 0, l
    while i < len1 and j < len2:
        comparisons += 1
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        accesses += 1
        k += 1

    while i < len1:
        arr[k] = left[i]
        i += 1
        k += 1
        accesses += 1

    while j < len2:
        arr[k] = right[j]
        j += 1
        k += 1
        accesses += 1

    return accesses, comparisons


def tim_sort(arr):
    MIN_RUN = 32
    n = len(arr)
    accesses, comparisons = 0, 0

    for start in range(0, n, MIN_RUN):
        end = min(start + MIN_RUN - 1, n - 1)
        accesses, comparisons = insertion_sort(arr, start, end, accesses, comparisons)

    size = MIN_RUN
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            accesses, comparisons = merge(arr, left, mid, right, accesses, comparisons)
        size *= 2

    return accesses, comparisons
