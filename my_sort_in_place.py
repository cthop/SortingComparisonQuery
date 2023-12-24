def my_sort_without_space(arr, left=0, right=None, minimum=None, maximum=None):
    if right is None:
        right = len(arr) - 1
    if left >= right:
        return
    if minimum is None or maximum is None:
        minimum, maximum = min(arr), max(arr)
    if minimum == maximum:
        return
    mid_point = (minimum + maximum) // 2
    i, j = left, right
    while i <= j:
        if arr[i] > mid_point:
            arr[i], arr[j] = arr[j], arr[i]
            j -= 1
        else:
            i += 1
    my_sort_without_space(arr, left, i - 1, minimum, mid_point)
    my_sort_without_space(arr, i, right, mid_point + 1, maximum)

