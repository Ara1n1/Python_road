"""
要求:
1.登录页面
2.学生概况页面 ID name 点击详情
3.学生详情页面 ID name age gender
"""
from flask import Flask, session, redirect, request, url_for
from flask_session import Session

from hm_detail import info
from hm_login import log
from hm_settings import DebugConfig
from hm_settings import EXEMPT_SET

app = Flask(__name__)
app.config.from_object(DebugConfig)
# app.config.from_object(TestConfig)

app.register_blueprint(log)
app.register_blueprint(log)
# app.register_blueprint(info)
Session(app)

app.session_interface

@app.before_request
def auth():
    if request.path in EXEMPT_SET:
        return
    if not session.get('username'):
        return redirect('/login')


@app.errorhandler(404)
def error404(error):
    return 'xxx'


"""url反向解析"""
@app.template_global()
def query(name, sid):
    return f'{url_for(name)}?sid={sid}'


if __name__ == '__main__':
    app.run()   # 基于tcp的socket连接


# app.__call__
# from werkzeug.serving import run_simple
from flask import request, request_tearing_down