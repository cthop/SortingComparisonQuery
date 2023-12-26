def my_sort_2(arr):
    if len(arr) <= 1:
        return arr
    return my_sort_2_util(arr, min(arr), max(arr))


MAX_BUCKETS = 100


def my_sort_2_util(arr, a, b):
    if len(arr) <= 1:
        return arr

    if a == b:
        return arr

    buckets_amount = min(len(arr), MAX_BUCKETS)
    buckets = [[[], b, a] for _ in range(buckets_amount)]

    for x in arr:
        idx = ((buckets_amount - 1) * (x - a)) // (b - a)
        buckets[idx][0].append(x)
        if x < buckets[idx][1]:
            buckets[idx][1] = x
        if x > buckets[idx][2]:
            buckets[idx][2] = x

    for i, (bucket, minima, maxima) in enumerate(buckets):
        buckets[i] = my_sort_2_util(bucket, minima, maxima)

    return [x for bucket in buckets for x in bucket]

# import random
# test_arr = [random.randint(0, 100) for _ in range(30)]
# print(sort(test_arr))
