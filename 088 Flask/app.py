import os

from flask import Flask, request, render_template, session, redirect
from markupsafe import Markup

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = '124$%^0354t#$%^&*()kfghjlE#$%^&BG$%3454567BH7'

STUDENT = {'name': 'Old', 'age': 20, 'gender': '中'}

STUDENT_LIST = [
    {'name': 'Old', 'age': 20, 'gender': '中'},
    {'name': 'henry', 'age': 18, 'gender': '男'},
    {'name': 'echo', 'age': 17, 'gender': '女'}
]

STUDENT_DICT = {
    1: {'name': 'Old', 'age': 20, 'gender': '中'},
    2: {'name': 'henry', 'age': 18, 'gender': '男'},
    3: {'name': 'echo', 'age': 17, 'gender': '女'}
}

# app.debug = True
from functools import wraps


def warpper(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get('username'):
            return func(*args, **kwargs)
        return redirect('/login')

    return inner


@app.template_global()
def ab(a, b):
    return a + b


def my_input(na, ty):
    html = f'<input type="{ty}" name="{na}" placeholder="customerize">'
    return Markup(html)


@app.route('/')
@warpper
def home():
    return 'AH, you are visiting Flask!'


@app.route('/index')
@warpper
def index():
    # return render_template('index.html')
    # return redirect('/')
    # return send_file('知乎.mp4')
    # return send_file('1.jpg')
    # return send_file('/Volumes/SANDISK/软件/Mounty.dmg')
    # info = {'k': 'v'}
    # return jsonify(info)
    return {'k': 'v'}


@app.route('/test')
@warpper
def test():
    li = ['method', 'url', 'args', 'values', 'host', 'path', 'files', 'form', 'data', 'json', 'cookies']
    count = 0
    for i in li:
        count += 1
        print(count, i, getattr(request, i))
    return 'ok'


@app.route('/login', methods=['GET', 'POST', ])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # username = request.form.get('username')
        # for i,j in request.form.items():
        #     print(i,j)
        # print(username)
        # """接收文件"""
        file = request.files.get('file_data')
        print(file, type(file))
        filepath = os.path.join('media', file.filename)
        file.save(filepath)
        if request.form.get('username') == 'henry':
            session['username'] = 'henry'
            return 'Login OK!'
        else:
            return 'failed'


@app.route('/jin_test')
def jin_test():
    # return render_template('jin_test.html', stu=STUDENT, stu_l=STUDENT_LIST, stu_d=STUDENT_DICT)
    # btn = Markup('<input type="text" name="test" placeholder=test>')
    btn = '<input type="text" name="test" placeholder=test>'
    return render_template('jin_test.html',
                           btn=btn,
                           stu=STUDENT,
                           stu_l=STUDENT_LIST,
                           stu_d=STUDENT_DICT,
                           ab=ab,
                           my_input=my_input,
                           )


if __name__ == '__main__':
    app.run()

