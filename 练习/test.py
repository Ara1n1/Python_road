#!/usr/bin/env python
# -*- coding:utf-8 -*-


ab_path = '/a/b/../c/./d'


def simplify_path(ab_path):
    re_path = ''
    for i in ab_path.split('/'):
        if i != '.' and i != '..':
            re_path += '/' + i
        elif i == '..':
            re_path = '/'.join(re_path.split('/')[:-1])
    return re_path.replace('/', '', 1)


res = simplify_path(ab_path)
print(res)

# numa, numb = (int(i) for i in (input('input two num: ').split(' ')))
# print(numa, numb)
# for i in range(numa, numb):
#     if i % 3 == 0:
#         i = 'foo' if i % 5 != 0 else 'foobar'
#     elif i % 5 == 0:
#         i = 'bar'
#     print(i, end=' ')
#
# numa, numb, numc = (int(i) for i in (input('input three num: ').split(' ')))
