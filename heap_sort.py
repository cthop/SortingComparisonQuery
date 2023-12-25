def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    accesses = 0
    comparisons = 0

    if left < n:
        comparisons += 1
        accesses += 2
        if arr[largest] < arr[left]:
            largest = left

    if right < n:
        comparisons += 1
        accesses += 2
        if arr[largest] < arr[right]:
            largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        accesses += 4
        child_accesses, child_comparisons = heapify(arr, n, largest)
        accesses += child_accesses
        comparisons += child_comparisons

    return accesses, comparisons


def heap_sort(arr):
    n = len(arr)
    total_accesses = 0
    total_comparisons = 0

    for i in range(n // 2 - 1, -1, -1):
        accesses, comparisons = heapify(arr, n, i)
        total_accesses += accesses
        total_comparisons += comparisons

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        total_accesses += 4
        accesses, comparisons = heapify(arr, i, 0)
        total_accesses += accesses
        total_comparisons += comparisons

    return total_accesses, total_comparisons
