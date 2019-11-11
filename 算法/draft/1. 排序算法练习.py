"""bubble sort"""


def bubble(li):
    for i in range(len(li), 1, -1):
        for j in range(1, i):
            if li[j - 1] > li[j]:
                li[j - 1], li[j] = li[j], li[j - 1]
    print(li, '<-- bubble sort')


"""insert sort """


def insert(li):
    i = 1
    while i < len(li):
        if li[i - 1] < li[i]:
            i += 1
        else:
            k = i
            while k > 0 and li[k - 1] > li[k]:
                li[k - 1], li[k] = li[k], li[k - 1]
                k -= 1
    print(li, '<-- insert sort')


"""select sort"""


def select(li):
    for j in range(len(li) - 1, 0, -1):
        max = 0
        for i in range(1, j + 1):
            if li[max] < li[i]:
                max = i
        li[max], li[j] = li[j], li[max]
    print(li, '<-- select sort')


"""quick sort"""


def quick(li, low, high):
    if low >= high:
        return
    left = low
    right = high
    base = li[left]

    while low < high:
        while low < high and li[high] > base:
            high -= 1
        li[low] = li[high]
        while low < high and li[low] < base:
            low += 1
        li[high] = li[low]
    li[low] = base
    quick(li, left, low - 1)
    quick(li, low + 1, right)


"""merge sort"""


def sort(left, right):
    c = list()
    l = h = 0

    while l < len(left) and h < len(right):
        print(left, right)
        if left[l] < right[h]:
            c.append(left[l])
            l += 1
        else:
            c.append(right[h])
            h += 1

    if l == len(left):
        for i in right[h:]:
            c.append(i)
    else:
        for i in left[l:]:
            c.append(i)
    return c


def merge(li):
    if len(li) <= 1:
        return li

    mid = len(li) // 2
    left = merge(li[:mid])
    right = merge(li[mid:])
    return sort(left, right)


if __name__ == '__main__':
    li = list(range(20, 0, -1))
    print(li)
    # bubble(li)
    # insert(li)
    # select(li)
    # quick(li, 0, len(li) - 1)
    # print(li, '<-- quick sort')

    li = merge(li)
    print(li, '<-- merge sort')
