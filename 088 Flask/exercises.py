"""
要求:
1.登录页面
2.学生概况页面 ID name 点击详情
3.学生详情页面 ID name age gender
"""
STUDENT_DICT = {
    1: {'name': 'Old', 'age': 38, 'gender': '中'},
    2: {'name': 'Boy', 'age': 73, 'gender': '男'},
    3: {'name': 'EDU', 'age': 84, 'gender': '女'},
}
from functools import wraps

from flask import Flask, request, render_template, redirect, session, url_for

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = '!@#^%$#@!@#*&&*()&*&NM:"FKhgdd;jGJFr  1`32nKJBKl;'


def warpper(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get('username'):
            return func(*args, **kwargs)
        return redirect('/login')

    return inner


@app.route('/login', methods=['GET', 'POST'])
@warpper
def login():
    if request.method == 'GET':
        return render_template('exec/login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'henry' and password == '123':
            session['username'] = 'henry'
            return redirect('/detail')
        return 'Failed'


@app.route('/detail', endpoint='hahaha')
@warpper
def detail():
    sid = request.args.get('sid')
    if sid:
        stus = {sid: STUDENT_DICT[int(sid)]}
        flag = {'flag': 0}
        return render_template('exec/detail.html', stus=stus, flag=flag)
    flag = {'flag': 1}
    return render_template('exec/detail.html', stus=STUDENT_DICT, flag=flag)


@app.route('/test')
def test():
    res = url_for('hahaha')
    print(res)
    return res


if __name__ == '__main__':
    app.run()

app.__call__()