#!/usr/bin/env python
# -*- coding:utf-8 -*-
# import time
# from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
#
#
# def func(i):
#     time.sleep(0.2)
#     return i
#
#
# tp = ThreadPoolExecutor(100)
"""
使用sumbit方法实现
"""
# res_l = []
# for i in range(100):
#     res = tp.submit(func, i)
#     res_l.append(res)
#
# for res in res_l:
#     print(res.result())

"""
使用map方法实现
"""

# res = tp.map(func, range(100))
# for i in res:
#     print(i)

"""
爬取网页并分析
"""
# import requests
# from concurrent.futures import ThreadPoolExecutor
#
#
# def get_page(url):
#     content = requests.get(url)
#     return {'url': url, 'content': content.text}
#
#
# def paraserpage(dic):
#     print(dic.result()['url'])
#
#
# url_l = ['https://www.baidu.com', 'https://www.meijutt.com/alltop_hit.html', 'https://www.cnblogs.com/henryw/',
#          'https://www.cnblogs.com']
# tp = ThreadPoolExecutor(3)
# for url in url_l:
#     ret = tp.submit(get_page, url)
#     ret.add_done_callback(paraserpage)


# from queue import PriorityQueue
# pq = PriorityQueue()
# pq.put((10, 'henry'))
# pq.put((6, 'echo'))
# pq.put((10, 'dean'))
# print(pq.get())
# print(pq.get())
# print(pq.get())
# print(pq.get())
