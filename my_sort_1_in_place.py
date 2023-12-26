def my_sort_1_in_place(arr):
    if len(arr) <= 1:
        return
    my_sort_1_in_place_util(arr, 0, len(arr) - 1, min(arr), max(arr))


def my_sort_1_in_place_util(arr, left, right, minimum, maximum):
    if left >= right:
        return

    if minimum == maximum:
        return

    mid = (minimum + maximum) // 2

    i, j = left, right
    left_maximum, right_minimum = minimum, maximum
    while i <= j:
        if arr[i] <= mid:
            if arr[i] > left_maximum:
                left_maximum = arr[i]
            i += 1
        else:
            if arr[i] < right_minimum:
                right_minimum = arr[i]
            arr[i], arr[j] = arr[j], arr[i]
            j -= 1

    my_sort_1_in_place_util(arr, left, i - 1, minimum, left_maximum)
    my_sort_1_in_place_util(arr, i, right, right_minimum, maximum)
