def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def bucket_sort(arr):
    if len(arr) <= 1:
        return arr

    # Finding minimum and maximum values
    min_value = min(arr)
    max_value = max(arr)

    # Handle the case where all elements are the same
    if min_value == max_value:
        return arr

    # Bucket initialization
    bucket_count = len(arr)
    buckets = [[] for _ in range(bucket_count)]

    # Distribute input array values into buckets
    for i in range(len(arr)):
        index = int((arr[i] - min_value) / (max_value - min_value) * (bucket_count - 1))
        buckets[index].append(arr[i])

    # Sort each bucket and concatenate
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(insertion_sort(bucket))

    return sorted_arr
