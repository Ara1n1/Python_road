#!/usr/bin/env python
# -*- coding:utf-8 -*-
from socket import *
ip_port = ('127.0.0.1', 9000)
bufsize = 1024

tcp_client = socket(AF_INET,SOCK_DGRAM)

while True:
    msg = input('请输入时间格式(例%Y %m %d)>>: ').strip()
    tcp_client.sendto(msg.encode('utf-8'), ip_port)

    data = tcp_client.recv(bufsize)


