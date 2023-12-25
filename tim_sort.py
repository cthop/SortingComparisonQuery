def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        temp = arr[i]
        j = i - 1
        while j >= left and arr[j] > temp:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = temp


def merge(arr, left, mid, right):
    len1, len2 = mid - left + 1, right - mid
    L = arr[left:left + len1]
    R = arr[mid + 1:mid + 1 + len2]

    i, j, k = 0, 0, left
    while i < len1 and j < len2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < len1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < len2:
        arr[k] = R[j]
        j += 1
        k += 1



def tim_sort(arr):
    min_run = 32
    n = len(arr)

    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort(arr, start, end)

    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            merge(arr, left, mid, right)
        size *= 2
