#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# # 进程池
# from multiprocessing import Pool
#
#
# def func(file):
#     with open(file,'r', encoding='utf8') as f:
#         text = f.read()
#     return text
#
#
# if __name__ == '__main__':
#     p = Pool(5)
#     for i in ['A.txt', 'B.txt']:
#         ret = p.apply(func, args=(i,))
#         print(ret)


# def consumer():  # 主-> 线程
#     r = 'yield '
#     while True:
#         n = yield r
#         if not n:
#             return
#         print('消费者 %s' % n)
#         r = '200 ok'
#
#
# def produce(c):  # 副-> 协程
#     c.send(None)
#     n = 0
#     while n < 5:
#         n += 1
#         print('生产者 %s...' % n)
#         r = c.send(n)
#         print('生产者 return=%s' % r)
#     c.close()
#
#
# c = consumer()  # <generator object consumer at 0x0000024CEE8B8830>
# produce(c)

# def func():
#     print(123)
#     n = yield ('aaa')
#     print('----->', n)
#     yield 'bbb'
#
#
# data = func()
# # print(data)
# v1 = next(data)
# print(v1)
# v = data.send('太厉害了，直接传进去了')
# print(v)


# from threading import Thread
#
#
# class Mythread(Thread):
#
#     def __init__(self, func, args=()):
#         self.func = func
#         self.args = args
#         super().__init__()
#
#     def run(self):
#         self.result = self.func(*self.args)
#
#     def get_result(self):
#         Thread.join(self)  # 等待线程执行完毕
#         try:
#             return self.result
#         except Exception:
#             return None
#
#
# def func(i):
#     # print(i)
#     return i
#
#
# th_l = []
# for i in range(5):
#     obj = Mythread(func, (i,))
#     obj.start()
#     res = obj.get_result()
#     print(res)

import gevent


def play():
    print("start play")
    gevent.sleep(1)
    print("end play")


# def sleep():
#     print("start sleep")
#     gevent.sleep(1)
#     print("end sleep")


g1= gevent.spawn(play)
g2 = gevent.spawn(play)
# gevent.joinall([g1, g2])
g1.join()
g2.join()
