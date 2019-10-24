import os

from flask import Blueprint, jsonify, send_file

from config import mongo, RET, COVER_PATH, MUSIC_PATH, QRCODE_PATH, CHAT_PATH

content = Blueprint('content', __name__)


@content.route('/content_list', methods=['post'])
def content_list():
    data_list = list(mongo.content.find({}))
    for index, info in enumerate(data_list):
        info['_id'] = str(info['_id'])
    RET['CODE'] = 0
    RET['MSG'] = '资源获取成功'
    RET['data'] = data_list

    return jsonify(RET)


@content.route('/get_cover/<filename>', methods=['get'])
def get_cover(filename):
    path_cover = os.path.join(COVER_PATH, filename)
    return send_file(path_cover)


@content.route('/get_music/<filename>', methods=['get'])
def get_music(filename):
    path_music = os.path.join(MUSIC_PATH, filename)
    return send_file(path_music)


@content.route('/get_qr/<filename>', methods=['get'])
def get_qr(filename):
    path_code = os.path.join(QRCODE_PATH, filename)
    return send_file(path_code)


@content.route('/get_chat/<filename>', methods=['get'])
def get_chat(filename):
    path_chat = os.path.join(CHAT_PATH, filename)
    print(path_chat)
    return send_file(path_chat)



