def my_sort_not_in_place(arr):
    if not arr:
        return 0, 0
    a, b = len(arr), len(arr)  # use of min and max
    _, accesses, comparisons = my_sort_not_in_place_util(arr, min(arr), max(arr), 0, 0)
    accesses += a
    comparisons += b
    return accesses, comparisons


def my_sort_not_in_place_util(arr, minimum, maximum, accesses, comparisons):
    if len(arr) <= 1:
        return arr, accesses, comparisons

    comparisons += 1
    if minimum == maximum:
        return arr, accesses, comparisons

    accesses += 2
    mid_point = (minimum + maximum) // 2

    left, right = [], []
    left_maximum, right_minimum = minimum, maximum
    for ele in arr:
        accesses += 1
        comparisons += 1
        if ele <= mid_point:
            comparisons += 1
            accesses += 1
            if ele > left_maximum:
                left_maximum = ele
            left.append(ele)
        else:
            comparisons += 1
            accesses += 1
            if ele < right_minimum:
                right_minimum = ele
            right.append(ele)

    sorted_left, accesses, comparisons = my_sort_not_in_place_util(left, minimum, left_maximum, accesses, comparisons)
    sorted_right, accesses, comparisons = my_sort_not_in_place_util(right, right_minimum, maximum, accesses,
                                                                    comparisons)

    return (sorted_left + sorted_right), accesses, comparisons
