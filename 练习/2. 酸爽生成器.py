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


"""面试1"""

# def iterator(x):
#     print(f'iter{x:03d}start')
#     res = []
#     for _ in range(0, x, 2):
#         res.append((_ ** 2) // 3)
#         yield res
#     print(f'iter{x:03d}finish')
#
#
# def main():
#     print('start')
#     _iter = iterator(6)
#     for _ in _iter:
#         print(_)
#         print('end')
#
#
# main()


"""面试2"""

def cor():
    data_list = []
    while True:
        print('go', end='')
        x = yield
        print(x)
        if x is None:
            break
        data_list.append(x)
    ret = sum(data_list) / len(data_list)

    print('average', ret)
    return ret


def main():
    print('call cor()')
    func = cor()
    print('next(func)')

    next(func)
    try:
        for x in range(3):
            print('->', x)
            func.send(x)

        func.send(None)

    except StopIteration as exp:
        # print(exp, type(exp))
        print('func return', exp.value)
        # pass


main()
"""面试2"""


# def check_func():
#     print('call check_func')
#     return True
#
#
# def check_before_run(func):
#     print('call decorator')
#
#     def func_wrapper(f):
#
#         def call_func(*args, **kwargs):
#             is_ok = func()
#             if is_ok:
#                 print('checked')
#                 return f(*args, **kwargs)
#             else:
#                 print('check failed')
#                 raise ImportError('check failed')
#         return call_func
#
#     return func_wrapper
#
#
# @check_before_run(check_func)
# def a_foo(name):
#     print('call a_foo ->', name)
#
#
# print('call a_foo start')
# a_foo('abc')
# print('call a_foo end')
