"""冒泡排序"""

li = [i for i in range(10, 0, -1)]
print(li)


def bubble_sort(li):
    # i 是需要多少个数就位
    for i in range(len(li), 1, -1):
        # j 是判断大小，并按需交换
        for j in range(1, i):
            if li[j - 1] > li[j]:
                li[j - 1], li[j] = li[j], li[j - 1]
    print(li, '<-- bubble_sort')


"""选择排序"""


def select_sort(li):
    for i in range(len(li) - 1, 0, -1):
        max = 0
        for j in range(i + 1):
            if li[j] > li[max]:
                max = j
        li[max], li[i] = li[i], li[max]
    print(li, '<-- select_sort')


"""插入排序"""


def insert_sort(li):
    i = 1
    while i < len(li):
        if li[i - 1] < li[i]:
            i += 1
        else:
            k = i
            while k >= 1 and li[k - 1] > li[k]:
                li[k], li[k - 1] = li[k - 1], li[k]
                k -= 1
    print(li)


"""快速排序"""


def quick_sort(li, low, high):
    if low >= high:
        return
    left = low
    right = high
    base = li[left]

    while low < high:
        while low < high and li[high] >= base:
            high -= 1
        li[low] = li[high]
        while low < high and li[low] < base:
            low += 1
        li[high] = li[low]
    li[low] = base
    # return low, high
    quick_sort(li, left, low - 1)
    quick_sort(li, low + 1, right)


"""归并排序"""


def merge(a, b):
    c = []
    h = j = 0
    while j < len(a) and h < len(b):
        if a[j] < b[h]:
            c.append(a[j])
            j += 1
        else:
            c.append(b[h])
            h += 1

    c.extend(b[h:]) if j == len(a) else c.extend(a[j:])
    return c


def merge_sort(lists):
    if len(lists) <= 1:
        return lists
    middle = len(lists) // 2
    left = merge_sort(lists[:middle])
    right = merge_sort(lists[middle:])
    return merge(left, right)


if __name__ == '__main__':
    # bubble_sort(li)
    # select_sort(li)
    # insert_sort(li)
    # quick_sort(li, 0, len(li) - 1)
    # print(li, '<-- quick_sort')

    merge_sort(li)
    print(li, '<-- merge_sort')
