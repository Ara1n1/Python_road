# -*- coding: utf-8 -*-
# __author__ = "maple"

import select
import selectors
# 操作系统提供
# 为了提高网络操作的并发效果，并且减少CPU的使用率才被推出的一个工具
# select poll epoll
# windows select
# linux select poll epoll
import socket
import time

sk = socket.socket()
sk.setblocking(False)
sk.bind(('127.0.0.1', 9000))
sk.listen()

rlst = [sk]
while True:
    print(len(rlst))
    try:
        rl, wl, el = select.select(rlst, [], [])
    except:
        print(rlst)
    # print('-->', rl)
    for obj in rl:
        if obj is sk:
            conn, _ = obj.accept()
            rlst.append(conn)

        else:
            msg = obj.recv(1024)
            if msg:
                # print(msg)
                obj.send(msg)
                # time.sleep(5)
            else:
                rlst.remove(obj)
