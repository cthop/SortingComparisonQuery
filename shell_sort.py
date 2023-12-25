def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    accesses, comparisons = 0, 0

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            accesses += 1

            j = i
            while j >= gap:
                comparisons += 1
                accesses += 1
                if arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    accesses += 2
                    j -= gap
                else:
                    break

            arr[j] = temp
            accesses += 1
        gap //= 2

    return accesses, comparisons
