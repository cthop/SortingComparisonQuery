def my_sort_not_in_place(arr):
    if not arr:
        return arr
    return my_sort_not_in_place_util(arr, min(arr), max(arr))


def my_sort_not_in_place_util(arr, minimum, maximum):
    if len(arr) <= 1:
        return arr

    if minimum == maximum:
        return arr

    mid = (minimum + maximum) // 2

    left, right = [], []
    left_maximum, right_minimum = minimum, maximum
    for ele in arr:
        if ele <= mid:
            if ele > left_maximum:
                left_maximum = ele
            left.append(ele)
        else:
            if ele < right_minimum:
                right_minimum = ele
            right.append(ele)

    sorted_left = my_sort_not_in_place_util(left, minimum, left_maximum)
    sorted_right = my_sort_not_in_place_util(right, right_minimum, maximum)

    return sorted_left + sorted_right
