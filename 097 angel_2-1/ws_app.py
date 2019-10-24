import json

from flask import Flask, request
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
from geventwebsocket.websocket import WebSocket

ws = Flask(__name__)

web_socket = {}


@ws.route('/app/<user_id>')
def app(user_id):
    app_socket = request.environ.get('wsgi.websocket')  # type:WebSocket
    web_socket[user_id] = app_socket
    print('建立app_socket连接', app_socket, user_id)
    while True:
        try:
            # 收发数据
            msg = app_socket.receive()
            msg_info = json.loads(msg)
            receiver = msg_info.get('to_user')
            receiver_socket = web_socket.get(receiver)
            receiver_socket.send(msg)
        except:
            pass


@ws.route('/toy/<toy_id>')
def toy(toy_id):
    toy_socket = request.environ.get('wsgi.websocket')  # type:WebSocket
    web_socket[toy_id] = toy_socket
    print('保持toy_socket连接。。。', toy_socket, toy_id)
    while True:
        try:
            msg = toy_socket.receive()
            msg_info = json.loads(msg)
            receiver = msg_info.get('to_user')
            receiver_socket = web_socket.get(receiver)
            receiver_socket.send(msg)
        except:
            pass


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 9528), ws, handler_class=WebSocketHandler)
    http_server.serve_forever()
