def quick_sort(arr, max_depth=100):
    quick_sort_helper(arr, 0, len(arr) - 1, 0, max_depth)


def quick_sort_helper(arr, low, high, depth, max_depth):
    if low < high:
        if depth > max_depth:
            insertion_sort(arr, low, high)
        else:
            pi = partition(arr, low, high)
            quick_sort_helper(arr, low, pi - 1, depth + 1, max_depth)
            quick_sort_helper(arr, pi + 1, high, depth + 1, max_depth)


def partition(arr, low, high):
    pivot_index = (low + high) // 2
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]

    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def insertion_sort(arr, low, high):
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
