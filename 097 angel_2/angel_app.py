from flask import Flask, request

from serv.content import content
from serv.devices import devices
from serv.friends import friend
from serv.uploader import uploader
from serv.users import users

app = Flask(__name__)
app.debug = True
app.register_blueprint(users)
app.register_blueprint(content)
app.register_blueprint(devices)
app.register_blueprint(friend)
app.register_blueprint(uploader)

"""调用生成toys的二维码函数"""
# from QRcreate import get_code
# get_code(5)
# from config import mongo
# mongo.toys.insert_one({'device_key':'b7903ce41d80353c8eb1e0ef6af9017e'})


if __name__ == '__main__':
    app.run('0.0.0.0', 9527)
