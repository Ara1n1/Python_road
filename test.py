from __future__ import unicode_literals

print('\'xxx\' is unicode?', isinstance('xxx', unicode))
print('u\'xxx\' is unicode?', isinstance(u'xxx', unicode))
print('\'xxx\' is str?', isinstance('xxx', str))
print('b\'xxx\' is str?', isinstance(b'xxx', str))
# f = lambda n: f(n - 1) * n if n >= 2 else 1
# print(f(5))

# def func1():
#     print('xxxx')
#     yield 1
#
#
# def func2():
#     g = func1()
#     print(next(g))
#     try:
#         ret = next(g)
#     except StopIteration as e:
#         print(e.value)
#
# func2()

# for i in range(1, 5):
#     print({item[i]: None for item in [{1: 1}, {2: 2}, {3: 3}, {4: 4}]})

# def outer(data):
#     def inner():s
#         print(data)
#
#     return inner
#
#
# li = []
# for i in range(10):
#     li.append(outer(i))
#
# li[0]()
# li[1]()
#
# li = [1, 2, 3]
# s = {1,2,3}
# print(s + s)
# import sys
#
# a = {1: 1}
# print('----', sys.getrefcount(a))
# print(sys.argv)
#
#
# def func(arg):
#     print(id(arg))
#     print(id(a))
#
#
# func(a)

# class Singleton(object):
#     __instance = None
#
#     def __new__(cls, *args, **kwargs):
#         from threading import Lock
#         with Lock():
#             if not cls.__instance:
#                 cls.__instance = object.__new__(cls)
#             return cls.__instance
#
#     def __init__(self, name):
#         self.name = name
#
#
# obj1 = Singleton('henry')
# obj2 = Singleton('echo')
# print(id(obj1), id(obj2))
#
#
# li = [1, 2, 3]
# print(li.__dir__())w
#
# print(iter(li).__next__())

# ret = filter(lambda n: n % 3 == 0, range(10))
# print(list(ret))
# print(list(ret))


# v = [1]
# v.append(v)
# print(len(v))


# import time
# from multiprocessing import Process
#
#
# def son1():
#     while True:
#         print('is alive')
#         time.sleep(0.5)
#
#
# def son2():
#     for i in range(5):
#         print('in son2')
#         time.sleep(1)
#
#
#
#
# if __name__ == '__main__':
#     p = Process(target=son1)
#     p.daemon = True
#     p.start()
#     p2 = Process(target=son2)
#     p2.start()
#     time.sleep(2)

#
# f = open('a.txt', mode='a', encoding='utf8')
# f.write('a')
# f.close()
# import logging
#
# logging.basicConfig(fielname='cmdb.log',
#                     format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
#                     datefmt='%Y-%m-%d-%H-%M-%S',
#                     level=logging.WARNING
#                     )
