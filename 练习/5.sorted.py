#!/usr/bin/env python
# -*- coding:utf-8 -*-


li = [-1, -2, 4, 3, 1]
info = {'a': 2, 'b': 10, 'c': 5}
l = sorted(li, key=abs, reverse=True)
info = dict(sorted(info.items(), key=lambda k: info[k[0]]))
print(l)
print(info)

# li = [1, 2, 3, 4, 5]
# info = {'a': 1, 'b': 2}
# v = info.fromkeys(li, 'hello')
# print(v, info)

# v = dict.fromkeys(['k1', 'k2'], [])
# v['k1'].append(666)
# print(v)
# v['k1'] = 777
# print(v)

# li = [1, 1, 2, 2, 3, 4, 5]
# li = list(set(li))
# print(li)


s = u'abc'
print(type(s))