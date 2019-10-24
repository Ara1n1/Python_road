from bson import ObjectId
from flask import Blueprint, request

from config import mongo, RET

users = Blueprint('users', __name__)


@users.route('/reg', methods=['post'])
def reg():
    user_info = request.form.to_dict()
    # print(user_info)
    user_info['avatar'] = 'baba.jpg' if user_info['gender'] == '2' else 'mama.jpg'
    user_info['bind_toys'] = []
    user_info['friend_list'] = []
    mongo.users.insert_one(user_info)
    RET['CODE'] = 0
    RET['MSG'] = '注册成功'
    RET['DATA'] = {}
    return RET


@users.route('/login', methods=['post'])
def login():
    user_info = request.form.to_dict()
    # print(user_info)
    user = mongo.users.find_one(user_info, {'password': 0})
    # print(user, type(user))
    user['_id'] = str(user['_id'])
    user.setdefault('chat', {'count': 0})

    if user:
        RET['CODE'] = 0
        RET['MSG'] = '登录成功'
        RET['DATA'] = user
    else:
        RET['CODE'] = -1
        RET['MSG'] = '用户名或密码错误'
    # print(RET)
    # RET['DATA']['avatar'] = 'mama.jpg'
    return RET


@users.route('/auto_login', methods=['post'])
def auto_login():
    user_id = request.form.to_dict().get('_id')
    # print(user_id)
    user = mongo.users.find_one({'_id': ObjectId(user_id)}, {'password': 0})
    user['_id'] = str(user['_id'])
    user.setdefault('chat', {'count': 0})

    RET['CODE'] = 0
    RET['MSG'] = '自动登录成功'
    RET['DATA'] = user
    # print('自动登录', RET)
    return RET
