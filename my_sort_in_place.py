def my_sort_in_place(arr):
    if not arr:
        return 0, 0
    a, b = len(arr), len(arr)  # use of min and max
    accesses, comparisons = my_sort_in_place_util(arr, 0, len(arr) - 1, min(arr), max(arr))
    accesses += a
    comparisons += b
    return accesses, comparisons


def my_sort_in_place_util(arr, left, right, minimum, maximum):
    accesses = 0
    comparisons = 0

    if left >= right:
        return accesses, comparisons

    if minimum == maximum:
        return accesses, comparisons

    mid_point = (minimum + maximum) // 2

    i, j = left, right
    left_maximum, right_minimum = minimum, maximum

    while i <= j:
        comparisons += 1
        accesses += 1
        if arr[i] <= mid_point:
            if arr[i] > left_maximum:
                left_maximum = arr[i]
            i += 1
        else:
            if arr[i] < right_minimum:
                right_minimum = arr[i]
            arr[i], arr[j] = arr[j], arr[i]
            accesses += 4
            j -= 1

    left_accesses, left_comparisons = my_sort_in_place_util(arr, left, i - 1, minimum, left_maximum)
    right_accesses, right_comparisons = my_sort_in_place_util(arr, i, right, right_minimum, maximum)

    accesses += left_accesses + right_accesses
    comparisons += left_comparisons + right_comparisons

    return accesses, comparisons
