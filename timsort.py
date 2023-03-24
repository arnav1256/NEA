def calc_min_run(n):  # finds run length for timsort algorithm
    r = 0
    while n >= 32:
        r |= n & 1
        n >>= 1
    return n + r


def insertion(array, start, end):  # binary insertion sort
    for i in range(start + 1, end + 1):
        item = array[i]
        pos = binary_search(array, item, start, i - 1)  # binary search to find position to insert item
        for j in range(i - 1, pos - 1, -1):  # shift elements to the right to make space for item
            array[j + 1] = array[j]
        array[pos] = item  # insert item into its correct position


def binary_search(array, item, start, end):  # binary search to find position to insert element
    if start > end:  # base case if item not found in list
        return start
    mid = (start + end) // 2  # middle element
    if array[mid] < item:
        return binary_search(array, item, mid + 1, end)  # recursively searches the right half
    elif array[mid] > item:
        return binary_search(array, item, start, mid - 1)  # recursively searches the left half
    else:
        return mid  # middle item is the correct position; base case if item is in list


def merge(arr, start, mid, end):  # merges 2 runs of sorted elements
    start2 = mid + 1
    if arr[mid] <= arr[start2]:  # 2 runs are already sorted
        return
    while start <= mid and start2 <= end:  # iterates through both lists
        if arr[start] <= arr[start2]:  # no switching required; advance first pointer
            start += 1
        else:
            value = arr[start2]
            index = start2
            while index != start:  # shift elements to the right to make space for item
                arr[index] = arr[index - 1]
                index -= 1
            arr[start] = value
            start += 1  # update pointers
            mid += 1
            start2 += 1


def timsort(arr):
    n = len(arr)
    min_run = calc_min_run(n)  # finds run length
    for start in range(0, n, min_run):  # divides the array into runs of length n
        end = min(start + min_run - 1, n - 1)
        insertion(arr, start, end)  # does binary insertion sort on each run
    while min_run < n:  # merges all the runs into fully sorted list
        for left in range(0, n, 2 * min_run):
            mid = min(n - 1, left + min_run - 1)
            right = min((left + 2 * min_run - 1), (n - 1))
            if mid < right:
                merge(arr, left, mid, right)
        min_run = 2 * min_run  # increases run size; after merging the runs double in size
    return arr
