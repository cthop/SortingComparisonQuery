def my_sort_with_space(arr, minimum=None, maximum=None):
    if len(arr) <= 1:
        return arr

    minimum = min(arr) if minimum is None else minimum
    maximum = max(arr) if maximum is None else maximum

    if minimum == maximum:
        return arr

    mid_point = (minimum + maximum) // 2

    left, right = [], []
    left_maximum = right_minimum = None
    for ele in arr:
        if ele <= mid_point:
            if left_maximum is None or ele > left_maximum:
                left_maximum = ele
            left.append(ele)
        else:
            if right_minimum is None or ele < right_minimum:
                right_minimum = ele
            right.append(ele)

    return my_sort_with_space(left, minimum, left_maximum) + my_sort_with_space(right, right_minimum, maximum)
