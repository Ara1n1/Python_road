# -*- coding: utf-8 -*-
# __author__ = "maple"
import socket
import threading
import time


def func():
    sk = socket.socket()
    sk.connect(('127.0.0.1', 9000))
    while True:
        sk.send(b'hello')
        msg = sk.recv(1024)
        print(msg)
        time.sleep(20)


for i in range(1500):
    threading.Thread(target=func).start()
