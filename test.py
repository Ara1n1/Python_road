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
# print(li.__dir__())
#
# print(iter(li).__next__())

# ret = filter(lambda n: n % 3 == 0, range(10))
# print(list(ret))
# print(list(ret))


v = [1]
v.append(v)
print(len(v))
