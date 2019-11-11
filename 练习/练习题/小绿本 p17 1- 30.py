#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""p3-17"""

s = "hello {}".format('henry')

"""
43. 将list按照下列规则排序，补全代码
"""
# li = [7, -8, 5, 4, 0, -2, -5]
# print(sorted(li, key=lambda x: [x < 0, abs(x)]))

"""
50. 现有字典d={"a":26,"g":20,"e":20,"c":24,"d":23,"f":21,"b":25} 请按照字段中的value字段进行排序
"""
# d = {"a": 26, "g": 20, "e": 20, "c": 24, "d": 23, "f": 21, "b": 25}
# print(sorted(d.items(), key=lambda x: x[1]))

"""
56.从0-99这100个数中随机取出10个, 要求不能重复, 可以自己设计数据结构
"""
# import random
# li = random.sample(range(100), k=10)
# print(li)


"""
57. python 判断一个字典中是否有这些key: "AAA",'BB','C',"DD",'EEE'(不使用for while)
"""
dic = {'AAA': 1, 'BB': 2, 'CC': 3, 'DD': 4}
li = ["AAA", 'BB', 'C', "DD", 'EEE']
s1 = set(dic.keys())
s2 = set(li)
# print(s1 & s2)

"""
58. 有一个list["This","is","a","Boy","!"], 所有元素都是字符串, 对他进行大小写无关的排序
"""
li = ['This', 'is', 'a', 'boy']

li = [i.lower() for i in li]
li.sort()
# print(li)

"""
70. 用Python实现99乘法表(用两种不同的方法实现)
"""
# [print(f'{i}*{j}={i*j}', end='\t') if i != j else print(f'{i}*{j}={i*j}', '\n') for i in range(1, 10) for j in range(1, i+1)]

# for i in range(1, 10):
#     for j in range(1, i+1):
#         if j == i:
#             print(f'{i}*{j}={i*j}', '\n')
#         else:
#             print(f'{i}*{j}={i*j}', end='\t')


"""
76. a=dict(zip(('a', 'b', 'c', 'd', 'e'), (1,2,3,4,5))) 请问a是什么？
"""
a = dict(zip(('a', 'b', 'c', 'd', 'e'), (1, 2, 3, 4, 5)))
# print(a)


"""
108. 输出结果是
"""
import math

# print(math.floor(5.5))

"""

"""


"""
1.进制转换
"""
# print(int('0b1111011', base=2))
# print(bin(18))
# print(int('011', base=8))
# print(int('0x12', base=16))
# print(hex(87))


"""
2.python递归的最大深度为1000
"""

"""
3.列举常见的内置函数
"""
# 强制转换：int， bool， str， list， tuple， dict， set
# 输入输出：print， input
# 进制转换：bin， oct， int， hex
# 数学相关：abs， max， min， float， round， divmod， sum
# map/filter/reduce/zip
# 编码相关：chr， ord
# 其他：len， type， id， range， open


"""
4. filter, map, reduce 的作用
"""
# filter，对可迭代对象根据指定标准进行数据筛选
# map，对可迭代对象进行批量的修改
# reduce，对可迭代对象进行指定运算

"""
5. 一行实现9*9乘法表
"""
# [print('%s*%s ' % (i, j,)) if i == j else print('%s*%s ' % (i, j,), end='') \
#  for i in range(1, 10) for j in range(1, i+1)]


"""
6. 什么是闭包
"""
# 闭包就是能够读取其他函数内部变量的函数。
# 在本质上，闭包是将函数内部和函数外部连接起来的桥梁。


"""
7.简述生成器、迭代器、装饰器以及应用场景
"""
# 生成器：主要用于构造大量数据时，为了节省内存空间，使用生成器可以在for 循环的时候一个个的生成数据
# 迭代器：for循环的内部就是通过迭代器的操作来实现
# 装饰器：用于调用其他函数或模块时，可以在其前后进行自定义操作


"""
8.使用生成器编写fib函数，函数声明为fib(max)，输入一个参数max值，是的函数可以这样调用
for i in range(0, 100):
    print(fib(1000))
"""
li = [1, 1]


def func(num=1000):
    a, b = 1, 1
    while a + b < num:
        b = li[-1] + li[-2]
        a = li[-2]
        li.append(b)
        yield b


for i in func():
    print(i)
#
# for i in range(100):
#     print(fib(1000))


"""
9. 一行代码，通过filter和lambda函数输出以下列表索引为基数对应的元素
"""
# list_a = [12, 213, 22, 2, 2, 2, 22, 2, 2, 32]
# print([i for i in filter(lambda i: i, list_a)])


"""
10. 写一个base62encode函数，把
"""
# result = []
# li = [str(i) for i in range(10)]
#
#
# def check_list():
#     i = 65
#     while i <= 90:
#         li.append(chr(i))
#         i += 1
#     i = 97
#     while 97 <= i <= 122:
#         li.append(chr(i))
#         i += 1
#
#
# def run():
#     while 1:
#         num = input('please input a num: ')
#         if not num.isdecimal():
#             print('your num is wrong')
#             continue
#         num = int(num)
#         return num
#
#
# def fun(count):
#     a, b = divmod(count, 62)
#     result.append(li[b])
#     if a > 62:
#         fun(a)
#     else:
#         if a:
#             result.append(str(a))
#         return ''.join(result[::-1])
#
#
# check_list()
# v = fun(run())
# print(v)


"""
11. 实现一个装饰器，限制该函数调用频率，如10s 一次
"""
# import time
#
#
# def wrapper(func):
#     start = 0
#
#     def inner():
#         nonlocal start
#         if time.time() - start >= 10:
#             start = time.time()
#             v = func()
#             return v
#         else:
#             print('限制访问')
#
#
#     return inner
#
#
# @wrapper
# def function():
#     print('hello')
#
#
# while 1:
#     function()
#     time.sleep(1)

"""
12. 实现一个装饰器，通过一次调用函数重复执行5次
"""
# def outside(num):
#     def wrapper(func):
#         def inner():
#             v = []
#             for i in range(num):
#                 v.append(func())
#             return v
#         return inner
#     return wrapper
#
# @outside(5)
# def func():
#     print('hello, Python')
#
# func()


"""
13. python一行print出1-100偶数list，（list推导式，filter均可）
"""
# print([i for i in range(1, 101) if i % 2 == 0])
# print(list(filter(lambda i: i,  range(2, 101, 2))))
# print(list(filter(lambda i: i if i % 2==0 else None,  range(1, 101))))


"""
14.解释生成器与函数的不同，并实现和简单使用generator
"""

# 1.语法上和函数类似：生成器函数和常规函数几乎一模一样的,他们都是使用def语句进行定义，
# \区别在于，生成器使用yield语句返回一个值，而常规函数使用return语句返回一个值
# 2.自动实现迭代器的协议：对于生成器，python自动实现迭代器协议，所以我们可以调用它的next
# \方法，并且在没有值返回的时候，生成器自动生成Stopltwration异常
# 3.状态挂起，生成器使用yield语句返回一个值.yield语句挂起该生成器函数的状态，保留足够的信息，
# \方便之后离开的地方继续执行


# def g():
#     print('one')
#     yield 'two'
#
#
# g1 = g()
# print(g1.__next__())

# for i in [1, 2, 3, 4].__iter__():
#     print(i)

"""
15. [i % 2 for i in range(10)] 和(i % 2 for i in range(10))
"""
# print([i % 2 for i in range(10)])
# print(list(i % 2 for i in range(10)))

"""
16. map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9])
"""
# print(list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9])))


"""
17. python定义函数时，如何书写可变参数和关键字参数
"""
# def func(*args, k=5, **kwargs):
#     pass


"""
18. Python3.5中enumerate的意思是什么
"""
# 枚举，在使用enumera函数时，至少需要传入一个可迭代对象,通过迭代一一取出同时为
# \每个元素添加一个序号，默认为0开始，也可以在传参时指定
# def enumerate(sequence, start=0):
#     n = start
#     for elem in sequence:
#         yield n, elem
#         n += 1
# 等价于
# for i in enumerate(range(100)):
#     print(i)


"""
19. 说说python中的装饰器，迭代器的用法，描述dict的item方法与iteritems方法的不同
"""
# 装饰器：为了在调用一些模块或函数时，在其前后进行自定义化操作时使用
# 迭代器：主要用于可迭代对象，可以通过迭代器一一获取可迭代对象中的元素
# dict.items 是一个list
# dict.iteritems 是一个<type 'dictionary-itemiterator'>的迭代器


# info = {'1': 1, '2': 2, '3': 3}
# val = info.iteritems()
# help (val)
# print(type(val))
# for i, j in val:
#     print i, j


"""
20. 是否使用过functools中的函数，其作用是什么
"""
# functools.partial
# functools.reduce
# functools.wrap(func)   # 装饰器一般需要使用，彻底装饰一个行数



"""
21. 如何判断一个值是函数还是方法
"""
# 1. 根据定义参数，方法有一个self形参，函数没有
# 2. 根据调用方式不同，函数调用是fun()，方法一般需要对象调用
# from types import MethodType, FunctionType
# def f():
#     pass
# print(isinstance(f, FunctionType))

"""
22. 请编写一个函数实现ip地址转换为和一个整数
"""
# ip = '192.168.12.87'
# res = int(''.join([bin(int(i)).replace('0b', '').zfill(8) for i in ip.split('.')]), base=2)
# print(res)

# def ip_transfer(ip):
#     print(int(''.join([bin(int(i)).replace('0b', '').zfill(8) for i in ip.split('.')]), base=2))
#
#
# ip_transfer('192.168.12.87')


"""
23. lambda 表达式以及应用场景
"""
# lambda 表达式又称为匿名函数，主要用于替换简单函数缩减代码量

"""
24. pass作用
"""
# python语法需要，在不需做任何操作的情况下使用

"""
25. *arg 和 **kwargs作用
"""
# 在定义函数时一般使用这两个参数
# *arg可以接收无限个位置参数形成一个元组
# **kwargs可以接收无限个关键字参数形成一个字典

"""
26. 如何在函中设置一个全局变量
"""
# 使用global关键字，先找到改变量，在进行赋值操作


"""
27. 看代码写结果
"""
# # 示例1
# def func(a, b=[]):
#     b.append(a)
#     print(b)
#
#
# func(1)
# func(1)
# func(1)
# func(1)
#
# # [1] [1, 1] [1, 1, 1] [1, 1, 1, 1]
#
# # 示例2
# def func(a, b={}):
#     b[a] = 'v'
#     print(b)
#
#
# func(1)
# func(2)
#
# # {1: 'v'}
# # {1: 'v', 2: 'v'}


"""
28. 看代码写结果：lambda
"""
# def num():
#     return [lambda x: i * x for i in range(4)]
#
#
# print([m(2) for m in num()])

# [6, 6, 6, 6]


"""
29. 简述yield和yield from 关键字
"""
# yield：用于定义生成器函数，yield后的值在for循环的时候会生成
# yield from：用于生成器函数中，调用其他函数或生成器函数, python3之后


"""
30. 有processFunc变量，初始化为processFunc = collapse  and (lambda s:''.join(s.split()))) or (lambda s:s)
"""
# collapse = True
# processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s:s)
# print(processFunc('i\tam\ntest\tobject !'))
#
# collapse = False
# processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s:s)
# print(processFunc('i\tam\ntest\tobject !'))


