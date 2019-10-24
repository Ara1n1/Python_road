from bson import ObjectId
from flask import Blueprint, request, jsonify

from config import mongo, RET

friend = Blueprint('friend', __name__)


@friend.route('/friend_list', methods=['post'])
def friend_list():
    user = request.form.to_dict()
    friend_info = mongo.users.find_one({'_id': ObjectId(user.get('_id'))})

    RET['CODE'] = 0
    RET['MSG'] = '好友查询'
    RET['DATA'] = friend_info.get('friend_list')
    return jsonify(RET)


@friend.route('/chat_list', methods=['post'])
def chat_list():
    chat_info = request.form.to_dict()
    chat_id = chat_info.get('chat_id')
    chat_win = mongo.chats.find_one({'_id': ObjectId(chat_id)})

    RET['CODE'] = 0
    RET['MSG'] = '查询聊天记录'
    RET['DATA'] = chat_win.get('chat_list')[-1:]

    return jsonify(RET)


@friend.route('/recv_msg', methods=['post'])
def recv_msg():
    from_user = request.form.get('from_user')
    chat_info = mongo.chats.find_one({'user_list': {'$all': [from_user]}})

    try:
        ret = chat_info.get('chat_list')[-1:]
    except:
        ret = [{'from_user': '', 'to_user': '', 'chat': 'nomessage.mp3', 'createTime': ''}]
    """如果没有消息需要进行下一步操作"""
    return jsonify(ret)
