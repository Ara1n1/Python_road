#!/usr/bin/env python
# -*- coding:utf-8 -*-

#
# def f(n: int):
#     if n == 1:
#         return 1
#     if n == 2:
#         return 2
#     if n == 3:
#         return 4
#     return f(n - 1) + f(n - 2) + f(n - 3)


# count = f(10)
# print(count)
#
# print(0b11110101 + 0b10100001)
#
# li1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# li2 = [9, 8, 7, 21, 13, 5, 2, 0]
# print(sum(set(li1[-7:-2] + li2)))

#
# def g(n):
#     for i in range(2, n):
#         if n % i == 0:
#             return False
#     return True
#
#
# li = [i for i in range(1, 30) if g(i)]
#
# print(li, sum(li))

#
# x = {'val': 1}
# y = {'val': 2}
# z = {'val': 3}
#
#
# def f(a, b):
#     a = {'val': 3}
#     b['val'] = 4
#     z = {'val': a['val'] + b['val']}
#
#
# f(x, y)
#
# print(x['val'], y['val'], z['val'])

# import copy
#
# a = [1, 2, 3, 4, 5, ['a', 'b', 'c']]
# b = a
# c = copy.copy(a)
# d = copy.deepcopy(a)
#
# a.append(5)
# a[5].append('d')
#
# print(b)
# print(c)
# print(d)

# class Parent(object):
#     x = 1
#
#
# class Child1(Parent):
#     pass
#
#
# class Child2(Parent):
#     pass
#
#
# Child1.x = 2
# print(Parent.x, Child1.x, Child2.x)
# Parent.x = 3
# print(Parent.x, Child1.x, Child2.x)

#
# a = 0.5
# while a != 1.0:
#     print a
#     a += 0.1
