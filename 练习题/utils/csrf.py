#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .myexception import MyException


class CrsfMiddleware(MyException):
    pass
    # def process(self, data):
        # return '【crs】%s【crs】' % data
