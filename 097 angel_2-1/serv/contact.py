from bson import ObjectId
from flask import Blueprint, request, jsonify

from config import RET, mongo

contact = Blueprint('contact', __name__)


# @contact.route('/req_list', methods=['post'])
# def req_list():
#     user_id = request.form.get('user_id')
#     user = mongo.request.find_one({'_id': ObjectId(user_id)})
#     user_bind_toy_list = user.get('bind_toys')
#     print(user_bind_toy_list)
#     return '200 ok'


@contact.route('/add_req', methods=['post'])
def add_req():
    request_info = request.form.to_dict()
    print(request_info)
    # request_info = {
    #      'add_user': '5d5a1a68787363ca84e72b82',
    #      'toy_id': '5d5a9f7ff1fd9ce71aab1aa2',
    #      'add_type': 'app',
    #      'req_info': '小粉球',
    #      'remark': '小懒猪'
    #  }
    toy_id = request_info.get('toy_id')
    if request_info.get('add_type') == 'toy':
        toy = mongo.toys.find_one({'_id': ObjectId(toy_id)})
        request_info['avatar'] = toy.get('avatar')
        request_info['nickname'] = toy.get('boby_name')
        request_info['status'] = 0
        request_info['toy_name'] = toy.get('toy_name')
    else:
        user = mongo.toys.find_one('_id')
        request_info['avatar'] = user.get('avatar')
        request_info['avatar'] = user.get('avatar')




        # # 创建chatwindow
    # chat = mongo.chats.insert_one({'user_list': [], 'chat_list': []})
    # chat_id = str(chat.inserted_id)
    # # 请求方的id
    # req_id = request_info.get('toy_id')
    # add_id = request_info.get('add_user')
    # # 查找请求和添加方对象
    # add_user = mongo.toys.find_one({'_id': ObjectId(add_id)})
    # req_user = mongo.toys.find_one({'_id': ObjectId(req_id)})
    #
    # # 添加方
    # add_user_info = {
    #     "friend_id": request_info.get('toy_id'),
    #     "friend_nick": req_user.get('baby_name'),
    #     "friend_remark": req_user.get('toy_name'),
    #     "friend_avatar": req_user.get('avatar'),
    #     "friend_chat": chat_id,
    #     "friend_type": "toy"
    # }
    #
    # # add_user['friend_list'].append(add_user_info)
    # # mongo.toys.update({'_id': ObjectId(add_id)}, {'$set': {'friend_list': add_user['friend_list']}})
    #
    # # 被添加方
    # req_user_info = {
    #     "friend_id": request_info.get('add_user'),
    #     "friend_nick": add_user.get('baby_name'),
    #     "friend_remark": add_user.get('toy_name'),
    #     "friend_avatar": add_user.get('avatar'),
    #     "friend_chat": chat_id,
    #     "friend_type": "toy"
    # }
    # # req_user['friend_list'].append(req_user_info)
    # # mongo.toys.update({'_id': ObjectId(req_id)}, {'$set': {'friend_list': req_user['friend_list']}})
    #
    # # print(add_user_info)
    # # print(req_user_info)

    RET['CODE'] = 0
    RET['MSG'] = '添加好友请求成功'
    RET['DATA'] = {}

    return jsonify(RET)
