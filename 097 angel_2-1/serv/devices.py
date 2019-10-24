from bson import ObjectId
from flask import Blueprint, request, jsonify, render_template

from config import RET, mongo

devices = Blueprint('devices', __name__)


@devices.route('/scan_qr', methods=['post'])
def scan_qr():
    qrcode_dict = request.form.to_dict()
    device = mongo.devices.find_one(qrcode_dict)
    # print(device)
    if not device:
        RET['CODE'] = 1
        RET['MSG'] = '请扫描玩具二维码'
        RET['DATA'] = {}
        return RET

    """用户扫描设备是我们的玩具，判断是否被用户绑定"""
    device_key = device['device_key']
    toy = mongo.toys.find_one({'device_key': device_key})
    # print(toy)
    if not toy:
        # 在toys表中没有查找到绑定设备
        RET['CODE'] = 0
        RET['MSG'] = '二维码扫描成功'
        RET['DATA'] = {
            "device_key": device_key
        }
    else:
        toy_id = str(toy['_id'])
        RET['CODE'] = 2
        RET['MSG'] = '设备已经进行绑定'
        RET['DATA'] = {
            "toy_id": toy_id
        }
    # print(RET)
    return RET


@devices.route('/bind_toy', methods=['post'])
def bind_toy():
    # 创建chatwindow
    chat = mongo.chats.insert_one({'user_list': [], 'chat_list': []})
    chat_id = str(chat.inserted_id)
    # print('私聊窗口的id：', chat_id)

    # 创建toy信息
    toy_info = request.form.to_dict()
    user_id = toy_info.pop('user_id')
    # print(user_id)
    user = mongo.users.find_one({'_id': ObjectId(user_id)})
    # print(user)
    toy_info['avatar'] = "toy.jpg"
    toy_info['bind_user'] = user_id
    toy_info["friend_list"] = []

    toy_friend_info = {
        'friend_id': toy_info['bind_user'],
        'friend_nick': user.get('nickname'),
        'friend_remark': toy_info.pop('remark'),
        'friend_avatar': user.get('avatar'),
        'friend_chat': chat_id,
        "friend_type": "app",

    }
    """作为测试使用"""
    # user['bind_toys'] = []
    # user['friend_list'] = []

    toy_info['friend_list'].append(toy_friend_info)
    # print('toy的数据', toy_info)
    toy = mongo.toys.insert_one(toy_info)
    toy_id = str(toy.inserted_id)

    user['bind_toys'].append(toy_id)
    user_friend_list = {
        'friend_id': toy_id,
        'friend_nick': toy_info.get('baby_name'),
        'friend_remark': toy_info.get('toy_name'),
        'friend_avatar': toy_info.get('avatar'),
        'friend_chat': chat_id,
        "friend_type": "toy",

    }
    user['friend_list'].append(user_friend_list)
    # print('用户好友', user_friend_list)
    # 更新 users 数据库中的数据
    # print(user['bind_toys'], user['friend_list'])
    mongo.users.update_one({'_id': ObjectId(user_id)},
                           {'$set': {'friend_list': user['friend_list'], 'bind_toys': user['bind_toys']}})
    # 更新 chats 数据库中的数据
    user_list = [user_id, toy_id]
    mongo.chats.update_one({'_id': chat.inserted_id}, {'$set': {'user_list': user_list}})
    RET['CODE'] = 0
    RET['MSG'] = '绑定成功'
    RET['DATA'] = {}
    return jsonify(RET)


@devices.route('/toy_list', methods=['post'])
def toy_list():
    user_id = request.form.get('_id')
    toy_list = list(mongo.toys.find({'bind_user': user_id}))
    for index, toy in enumerate(toy_list):
        toy['_id'] = str(toy.get('_id'))

    RET['CODE'] = 0
    RET['MSG'] = '获取玩具信息成功'
    RET['DATA'] = toy_list
    return jsonify(RET)


"""返回模拟玩具 web端"""


@devices.route('/web')
def web():
    return render_template('WebToy.html')


@devices.route('/open_toy', methods=['post'])
def open_toy():
    device_key = request.form.get('device_key')
    # print(device_key)

    # 如果没有玩具的二维码，玩具未授权
    ret = {}

    toy = mongo.toys.find_one({'device_key': device_key})
    if toy:
        ret['code'] = 0
        ret['music'] = "Success.mp3"
        ret['toy_id'] = str(toy.get('_id'))
        ret['name'] = str(toy.get('toy_name'))
    else:
        # print(ret)
        device = mongo.devices.find_one({'device_key': device_key})
        if device:
            ret['code'] = 1
            ret['music'] = "Nobind.mp3"
        else:
            # print('玩具未授权', ret)
            ret['code'] = 2
            ret["music"] = "Nolic.mp3"

    return jsonify(ret)
