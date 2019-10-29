#!/usr/bin/env python
# -*- coding:utf-8 -*-


# def func():
#     while True:
#         time.sleep(0.5)
#         print(os.getpid(), 'is func')
#
#
# if __name__ == '__main__':
#     p = Process(target=func)
#     p.daemon = True
#     p.start()
#     time.sleep(2)

from threading import Thread
from multiprocessing import Process
import time


def _wait():
    time.sleep(3)


# flag a
start = time.time()
t = Thread(target=_wait, daemon=True)

# t = Process(target=_wait, daemon=True)
t.start()
# flag b
endtime = time.time()
print(endtime - start)
