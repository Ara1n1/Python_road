#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
导入随机数列
"""
"""
随机数，会重复
"""
# from random_list import func
# li = func(0, 50, 20)

"""
逆序数列
"""
li = [i for i in range(20, 0, -1)]

"""
查看要排序的数列
"""
# li = [i for i in range(20)]
# print(li)

"""
# way1
i = 0
while i < len(li):
    if i < 0 or li[i - 1] <= li[i]:
        i += 1
    else:
        li[i - 1], li[i] = li[i], li[i - 1]
        i -= 1

print(li)
"""

"""
# way2:improve
"""
# i = 1
# while i < len(li):
#     if i < 1 or li[i - 1] <= li[i]:
#         i += 1
#     else:
#         k = i
#         while 0 < k and li[k - 1] > li[k]:
#             li[k - 1], li[k] = li[k], li[k - 1]
#             k -= 1
#
# print(li)


"""
繁琐写法
"""
# i = 1
# k = 1
# while i < len(li):
#     i = k
#     if i < 1 or li[i - 1] <= li[i]:
#         i += 1
#         k = i
#     else:
#         while 0 < i and li[i - 1] > li[i]:
#             li[i - 1], li[i] = li[i], li[i - 1]
#             i -= 1
#
# print(li)


"""
冒泡排序
"""


class Bubble(object):

    def __call__(self, *args, **kwargs):
        for i in range(len(li) - 1):
            for i in range(len(li) - 1):
                if li[i] > li[i + 1]:
                    li[i], li[i + 1] = li[i + 1], li[i]
        print(li)

# li = Bubble()()

"""
冒泡排序改进：提前终止的bubble
"""
j = len(li) - 1


def swap(li):
    i = 1
    global j
    sorted = True
    while i < len(li):
        if li[i - 1] > li[i]:
            sorted = False
            li[i - 1], li[i] = li[i], li[i - 1]
        i += 1
    return sorted


def bubble(li):
    global j
    while j:
        j -= 1
        if swap(li):
            break
    print('哈哈，我是j，看我是不是0哦', 'j =', j)
    print(li)

# bubble(li)


"""
冒泡排序改进：提前终止的bubble + 脏位判断
"""
# last = 0
# j = len(li) - 1
# def swap(li):
#     i = 1
#     global last, j
#     print(last, end=' ')
#     sorted = True
#     while i < len(li) - j:
#         if li[i-1] > li[i]:
#             sorted = False
#             li[i - 1], li[i] = li[i], li[i - 1]
#             last = i
#         i += 1
#     return sorted
#
#
# def bubble(li):
#     global j
#     while j:
#         j -= 1
#         swap(li)
#     print('')
#     print('哈哈，我是j，看我是不是0哦', 'j =', j)
#
#
# bubble(li)
# print(li)


"""
验证
"""
flag = '正确'
for i in range(len(li) - 1):
    if li[i] > li[i + 1]:
        flag = '错误'
        break

# print(flag, li[i])

alist = [22, 13, 4, 6, 8, 9, 23, 45, 76, 1]

"""冒泡排序"""


def bubble(alist):
    for j in range(len(alist) - 1):
        for i in range(1, len(alist) - j):
            if alist[i - 1] > alist[i]:
                alist[i - 1], alist[i] = alist[i], alist[i - 1]
    print(alist)


# bubble(alist)
"""选择排序"""


def select(alist):
    for j in range(len(alist) - 1, 0, -1):
        max = 0
        for i in range(j):
            if alist[max] < alist[i + 1]:
                max = i + 1
        alist[max], alist[j] = alist[j], alist[max]
    print(alist)


# select(alist)


def sort(alist):
    for j in range(len(alist) - 1, 0, -1):
        max = 0
        for i in range(j):
            if alist[max] < alist[i + 1]:
                max = i + 1
        alist[max], alist[j] = alist[j], alist[max]
    print(alist)


def insert(alist):
    i = 1
    while i < len(alist):
        if alist[i - 1] < alist[i]:
            i += 1
        else:
            k = i
            while k > 1 and alist[k - 1] > alist[k]:
                alist[k - 1], alist[k] = alist[k], alist[k - 1]
                k -= 1
    print(alist)


# insert(alist)


# 最终代码
def sort(alist):
    gap = len(alist) // 2
    while gap >= 1:
        for i in range(gap, len(alist)):
            while i >= 1:
                if alist[i] < alist[i - gap]:
                    alist[i], alist[i - gap] = alist[i - gap], alist[i]
                    i -= gap
                else:
                    break
        gap //= 2
    print(alist)


# sort(alist)

# # 增量为gap的 shell sort
# def shell(alist):
#     gap = len(alist) // 2
#     i = gap
#     while gap:
#         while i < len(alist):
#             print(gap)
#             if alist[i - gap] < alist[i]:
#                 i += gap
#             else:
#                 # k = i
#                 # while k >= gap and alist[k - gap] > alist[k]:
#                 print(gap)
#                 alist[i - gap], alist[i] = alist[i], alist[i - gap]
#                 i -= gap
#         gap //= 2


# print(alist)
# shell(alist)
# print(alist)

"""快速排序"""


# def quick_sort(alist, left, right):
#     # 结束递归的条件
#     if left >= right:
#         return
#     low = left
#     high = right
#     base = alist[left]
#     while low < high:
#         while low < high and alist[high] > base:
#             high -= 1
#         alist[low] = alist[high]
#         while low < high and alist[low] <= base:
#             low += 1
#         alist[high] = alist[low]
#
#     alist[high] = base
#     quick_sort(alist, left, low - 1)
#     quick_sort(alist, low + 1, right)
#
#
# quick_sort(alist, 0, len(alist) - 1)
# print(alist)


def quick_sort(alist, left, right):
    if left >= right:
        return

    low = left
    high = right
    base = alist[low]
    while low < high:
        while low < high and base < alist[high]:
            high -= 1
        alist[low] = alist[high]

        while low < high and alist[low] <= base:
            low += 1
        alist[high] = alist[low]
    alist[low] = base
    quick_sort(alist, left, low - 1)
    quick_sort(alist, low + 1, right)


# alist = [5, 4, 3, 2, 1, 5, 3]
# quick_sort(alist, 0, len(alist) - 1)
# print(alist)

def bubble_sort(li):
    for i in range(len(li) - 1):
        for j in range(1, len(li) - i):
            if li[j - 1] > li[j]:
                li[j - 1], li[j] = li[j], li[j - 1]


li = [5, 4, 3, 2, 8, 2]


# bubble_sort(li)
# print(li)


def select_sort(li):
    for j in range(len(li) - 1, 0, -1):
        max = 0
        for i in range(j + 1):
            if li[max] < li[i]:
                max = i
        li[max], li[j] = li[j], li[max]
    print(li)


# select_sort(li)
