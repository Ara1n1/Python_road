#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
示例1
"""
# ret = filter(lambda n: n % 3 == 0, range(10))
# print(len(list(ret)))
# print(len(list(ret)))

"""
示例2
"""

# def add(n, i):
#     return n + i
#
#
# def test():
#     for i in range(4):
#         yield i
#
#
# g = test()
#
# for n in [1, 10, 20]:
#     g = (add(n, i) for i in g)
#
# print(list(g))

"""
示例3
"""

#
# def add(n, i):
#     return n + i
#
#
# def test():
#     for i in range(4):
#         yield i
#
#
# g = test()
# for n in [1, 10, 5]:
#     g = (add(n, i) for i in g)
#
# print(list(g))
