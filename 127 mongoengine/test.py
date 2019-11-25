#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

sys._getframe()


def test():
    pass
    print(sys._getframe(0).f_code.co_filename, sys._getframe(0).f_code.co_name)
    print(sys._getframe(1).f_code.co_filename, sys._getframe(1).f_code.co_name)
    print(sys._getframe(2).f_code.co_filename, sys._getframe(2).f_code.co_name)


def index():
    pass
    test()


def test2():
    index()


test2()
