def my_sort_3(arr):
    a, b = min(arr), max(arr)

    result = [[] for _ in range(b - a + 1)]

    for ele in arr:
        pos = ele - a
        result[pos].append(ele)

    return [x for bucket in result for x in bucket]
