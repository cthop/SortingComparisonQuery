def quick_sort(arr):
    accesses, comparisons = quick_sort_helper(arr, 0, len(arr) - 1, 0, 0)
    return accesses, comparisons


def quick_sort_helper(arr, low, high, accesses, comparisons):
    if low < high:
        pi, accesses, comparisons = partition(arr, low, high, accesses, comparisons)
        accesses, comparisons = quick_sort_helper(arr, low, pi - 1, accesses, comparisons)
        accesses, comparisons = quick_sort_helper(arr, pi + 1, high, accesses, comparisons)
    return accesses, comparisons


def partition(arr, low, high, accesses, comparisons):
    pivot_index = (low + high) // 2
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    accesses += 4

    pivot = arr[high]
    accesses += 1
    i = low - 1
    for j in range(low, high):
        comparisons += 1
        accesses += 1
        if arr[j] < pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
            accesses += 4
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    accesses += 4
    return i + 1, accesses, comparisons
