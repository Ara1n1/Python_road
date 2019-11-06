# -*- coding: UTF-8 -*-

from redis_helper import RedisHelper

obj = RedisHelper()
while True:
    msg = input('>>:')
    obj.public(msg)