

# 1. Flask基础

-   **flask理念**：一切从简为服务器减轻压力

## 1. 框架对比

| Django               | Flask                                              |
| -------------------- | -------------------------------------------------- |
| Admin - Model        | 原生无                                             |
| Model                | 原生无                                             |
| Form                 | 原生无                                             |
| **session**          | 有-颠覆认知(存储到服务端内存中，浏览器的cookies中) |
| 教科书式框架         | 第三方组件非常丰富。一切从简                       |
| **优势对比**         |                                                    |
| 组件、功能全，教科书 | 轻，快                                             |
| **劣势对比**         |                                                    |
| 占用资源，cpu，ram   | 先天不足，第三方组件稳定性较差                     |
| 创建项目复杂度高     |                                                    |

## 2. Flask安装

1. 安装：pip3 install Flask
   - 直接创建python文件
   - ps：不要使用工具中的插件创建Flask项目
2. 三行启动flask项目
3. Flask：框架源码
   - **Jinja2**：模版语言
   - **MarkupSafe**：render基于此，防止**xss**攻击
   - **Werkzeug**：类似django的uwsgi底层都是基于wsgi，承载flask服务，类似tomcat

## 3. 创建项目

### 1. 创建py文件

- 设置DEBUG：项目会自动重启

```python
from flask import Flask
# 命名
app = Flask('app.py')
# 或 app = Flask(__name__)
app.config['DEBUG'] = True
# 或 app.debug = True

@app.route('/')
def home():
  	return 'AH, you are visiting Flask-site!'

if __name__ == '__main__':
	# 监听地址和端口，默认是127.0.0.1:5000
	app.run('0.0.0.0', 5000)
# werkzeug调用run_simple
# wsgi处理请求头(网关接口)
# wsgi处理后的数据，environment。		
```

### 2. response

-  content type：浏览器根据此参数，判断响应类型

#### 1. "xxx"

- django中的 HttpResponse('hello')，Flask是 'hello'

```python
@app.route('/index')
def index():
  	return  'hello world i am Flask'
```

#### 2. render_template

- 响应模版，默认存放路径 templates，打开模版并替换，依赖包 MarkupSafe中的 Markup 发送给浏览器

```python
@app.route('/index')
def index():
  	return render_template('index.html')
```

#### 3. redirect

- 在Response Header中加入 Location: '/login'

```python
@app.route('/login')
def login():
  	return render_template('/index')
```

- **以上是web框架的三剑客**

#### 4. send_file()

- response instance：流媒体类型

- 打开文件并自动识别文件类型，在content-type中添加文件类型，content-type:文件类型
- **浏览器特性**：可识别的 content-type 自动渲染，不识别时，自动下载该文件

#### content-type(6)

1. `text/html`
2. `text/plain`，保留当前文件格式
3. `image/jepg`或者 `image/png`
4. `audio/mpeg：<video> ，应该是<audio>`，chrome完成
5. `video/mp4：<video>` 标签
6. `application/x-msdownload：xx.exe`

- 文件类型：一般是文件第一行就是文件类型

```python
from flask import send_file
@app.route('/get_file')
def get_file():
  	# 返回文件内容，自动识别文件类型
  	return send_file('app.py')
```

#### 5. jsonify

- flask 1.1.1 版本中，dict直接作为返回值返回，无须 jsonify
- **返回标准json格式字符串，api接口，先序列化字典，并设置content-type: Application/json**

```python
@app.route('/get_json')
def get_json():
  	d = {'k':'v'}
    return jsonify(d)
```

## 4. request(11)

- request在flask中是公共变量(顶头小写)，请求上下文保存机制
- 从reqeust中获取的数据类型为：ImmutableMultiDict([('id', '1')])

```python
# 请求方式和数据 5
1. request.method			# 获取请求的方式
2. request.form				# 获取 FormData 中数据(ajax)
   .to_dict()	  			# request.from.to_dict()：返回对应的字典
   							# 类型：ImmutableMultiDict([])
3. request.args				# 获取url中的参数
4. reqeust.values			# 获取 url 和 FormData 中的数据，如果key相同 url中的会覆盖 form中数据
							# CombinedMultiDict([ImmutableMultiDict([('id', '1')]), ImmutableMultiDict([])])
5. request.files			# 获取 Form 中文件，返回 FileStroage中有 save() 方法和 filename属性
	.save(文件路径)
    .filename

# 请求来源相关 3
6. request.host				# ip + port
7. request.path				# url路由地址
8. request.url				# 完整路径，如：http://127.0.0.1:5000/detail?id=2

# cookies相关 1
9. request.cookies			# 字典，获取浏览器请求时带上的cookies

# 特殊数据封装 3
10.request.data				# Content-type 中不包含 Form 或 FormData，保留请求体中的原始数据，b""类型
11.request.json				# 请求头的 Content-type:application/json
   							# 请求体中的数据被序列化到request.json中，以字典的形式存放
```

```python
from flask import Flask
app = Flask(__name__)

@app.route('/login', methods=['GET','POST',])
def login():
  	# 优先判断请求方式
    # 如果是GET请求
    if request.method == 'GET':
      	return render_template('login.html')
    # 如果是POST请求，获取 用户名，密码 校验
    else: # 405 请求方式不被允许
      	# request.form.to_dict()
        my_file = request.files.get('my_file')
        filename = my_file.filename
        filepath = os.path.join('avatar', filename)
        my_file.save(filepath)
        if request.form.get('username') == 'xxx':
          	return 'Login OK!'
    return '200 ok'

if __name__ == '__main__':
		app.run()
```

- ImmutableMultiDict类型数据用法和dict类型相同，都有 values(), items()，keys() 方法

## 5. Jinja2(5)

### 1.  与django不同(4)

1. {{ my_input(arg1, arg2...) }}：引用或执行，**函数必须有括号**
2. {% %}：逻辑，方法需要有()
3. dict类型可以使用 info['username']
4. 如果变量没有定义会报错

### 2. 传递变量(关键字传参)

```python
app.config['DEBUG'] = True
或 app.debug = True

@app.route('/')
def stu():
  	return render_template('stu.html', stu=STUDENT,)
app.run('0.0.0.0:9527')
```

### 3. 传递函数

- **@app.template_global()**：项目中任何地方都可以使用被装饰的函数

```python
@app.template_global()
def ab(a,b):
  	return a+b

@app.route('/a')
def homea():
  	return render_template('a.html', ab=ab)
```

### 4. 宏指令

- 在jinja2模版中使用

```jinja2
{% macro my_input(na, ty) %}
	<input type="{{ ty }}" name="{{ na }}">
{% endmacro %}
{{ my_input('username', 'text') }}
```

### 5. Markup

- 在view 函数中，生成标签在使用

```python
from markupsafe import Markup

@app.route('/a')
def homea():
  	inp = Markup("<input type='submit' value='xxx'>")
    return render_template('a.html', btn=inp)

def my_input(na, ty):
  	s = f"<input type='{ty}' value='{na}'>"
    return Markup(s)
```

```jinja2
{{ btn | safe }}
{{ my_input('username', 'text') }}
```

## 6. session(5)

1. **基于请求上下文**
2. 一般和 request 一起导入
3. **交由客户端保管机制**，加密后存到浏览器的cookies中。保存一串字符串
4. 原生：**不建议添加过多的 key:values**，健值对越多，浏览器需要保存的cookies越长，Flask会先对健值对进行压缩和加密
6. **flask-session：把加密后的session从浏览器，移动到服务端**

```python
from flask import session
# 密钥不能为空
app.secret_key = "1!@#$8943:''.,xvzn;5lk12@!lg)*743%^&"
# 装饰器

def warpper(func):
  	def inner(*args, **kwargs):
      	# 校验登录状态、校验session中有没有 user key
      	if session.get('user'):
          	return func()
        else:  # 校验失败，跳转到登录页面
          	return redirect('/login')
		return inner

@app.route('/login', methods=['GET', 'POST'])
def login():
  	if request.method == 'GET':
      	return render_template('login.html')
    else:
      	if request.form.get('username') == 'henry':
          	return 'Login OK!'
        else:
        		return 'failed'

@app.route('/')
@warpper
def homea():
    return render_template('a.html')
```

# 2. Flask项目

## 1. 路由

### 1. 装饰器装饰多个函数

1. 自定义装饰器最终会出现多个 inner 函数最终为 endpoint，flask中通过endpoint查找view
2. 基于functools 修改 `__name__`，functools.wraps，在装饰器的inner上添加`functors.wraps(func)`
3. 添加endpoint参数

```python
@app.route('/a', endpoint='end_a')
@warpper
def a():
    pass
  
@app.route('/b', endpoint='end_b')
@warpper
def b():
    pass
  
@app.route('/', endpoint='home')
@warpper
def home():
    pass
```

- endpoint值必须唯一

### 2. route参数(5)

#### 1. methods=[]/()

- 请求方式不区分大小写

```python
@app.route(rule, methods=['get', 'POST', 'options'])
```

- getatter() or ('GET', )
- set(item.upper() for item in methods)

#### 2. endpoint=None

- 解决装饰器不能装饰多个函数的问题
- **路由地址和endpoint的mapping**
- **路由地址和视图之间mapping**
- 默认是视图函数名

```python
@app.route('/', endpoint=None)
def home():
    return 'ok!'
```

#### 3. defaults={'count': 20}

- 默认参数
- path = url_for(**endpoint**)：返回路由地址

```python
from flask import Flask
url_for('end_a')
url_for('home')
# {'end_a':'/a', 'home': '/'}
```

```python
@app.route(rule, endpoint=None, defaults={'count':20})
def home(count):
    count = request.args.get('count', count)
    return f'200 ok!{count}'
```

#### 4. strict_slashes=False

- 是否严格遵循地址匹配

```python
@app.route(rule, endpoint=None, strict_slashes=True)
def home():
    return f'200 ok!{count}'
```

#### 5. redirect_to='/'

- **永久重定向**，状态码，308/301
- 不进入视图函数，直接重定向

```python
@app.route(rule, endpoint=None, redirect_to='/')
```

### 3. 动态参数路由

- str：可以收一切，**默认是 string 类型**
- rule：`/home/<filename>`， `/home/<int:page>`， `/home/<ty>_<page>_<id>`，分页、获取文件、解决分类，**解决正则路由**
- send_file()：需要限定文件目录

```python
@app.route('/home/<int:page>', endpoint='home',)
def home(page):
    print(type(page))
    return '200 ok!'
  
@app.route('/home/<page>_<ty>_...', endpoint='home',)
def home(page, ty, ...):
    pass
  
@app.route('/home/<filename>', endpoint='home',)
def home(filename):
    return send_file(f'media/{filename}')
```

## 2. Flask配置

-   static_host=None：静态文件的服务器

### 1. 初始化配置(3)

#### 1. template_folder=''

- **指定模板存放路径**，默认时templates

```python
app = Flask(__name__, template_folder='templates')
```

#### 2. staic_folder='static'

- 锁定访问目录，静态文件存放目录，默认：static

```python
app = Flask(__name__, static_folder='img', static_url_path='/static')
# http://127.0.0.1:5000/static/1.jpeg
```

#### 3. static_url_path='/static'

- 静态文件访问路径，默认`/staic_folder`
- 自动拼接 host：`http://127.0.0.1:5000/`

```python
<img src='访问地址'>
<img src='static/1.jpg'>
```

- static_host=None：其他主机

- instance_path：多app

### 2. 实例配置(app配置)

#### 1. default_config

- **default_config** = {} ：默认配置
- 'TESTING'：True，日志级别为Debug，修改代码后不自动重启，错误环境不透传，接近生产环境
- ''：31days(默认)
- JSONIFY_MIMETYPE='application/json'

```python
# 开启 debug 模式，自动重启、透传错误信息、log级别较低 debug 级别
app.debug = True
# 使用session
app.secret_key = 'R&w34hr*&%^R7ysdjh9qw78r^*&A%863'
# session名称
app.session_cookie_name = 'ah'
# session生命周期，20s过期为 None
app.permanent_session_lifetime = 20
# respone头中content-type:xxx
app.config['JSONIFY_MIMETYPE']='xxx'
```

#### 2. settings.py

```python
import hashlib

class DubugConfig(object):
    DEBUG = True
    SECRET_KEY = '#$%^&fguyhij&^$EHBksdj`109u23'
    PERMANENT_SESSION_LIFETIME = 3600
    SESSION_COOKIE_NAME = 'ah'

class TestConfig(object):
    TESTING = True
    SECRET_KEY = hashlib.md5(f'{time.time()}#$%^&124:"hfag(&sfdgh3ir;dfguyhij&^$EHBksdj`109u23{time.time()}'.encode('utf-8')).hexdigest()
	PERMANENT_SESSION_LIFETIME = 360000
    SESSION_COOKIE_NAME = '$%^&124:"hfag('
```

#### 3. 配置生效

```python
from settings.py import DubugConfig,TestConfig
app.config.from_object(DubugConfig)
app.config.from_object(TestConfig)
```

## 3. Blueprint

- **不能被run的flask实例，不存在config**
- **app的功能隔离**
- **视图路由分割**

```python
from flask import Blueprint
# 蓝图标识必须唯一
bp = Blueprint('app01', __name__,url_prefix='/car')
or
bp = Blueprint(__name__, __name__,url_prefix='/car')

@bp.route('/user')
def user():
    return 'I am app01!'

# 或 bp.add_url_rule()
# 访问当前蓝图中的装饰器
@bp.before_request
@bp.after_request
@bp.errorhandler(Http错误码)
```

```python
from app01 import bp
app.register_blueprint(bp)
```

## 4. 特殊装饰器

- requset**校验没过时**，**绕过view 执行全部after_request**
- 只要有响应返回，af全部执行

### 1. @app.before_request

- 在请求进入视图函数之前，作出处理

```python
@app.before_reqeust
def be1():
    print('i am be1')
    
@app.before_reqeust
def be2():
    print('i am be2')
```

### 2. @app.after_request

- 在响应返回客户端之前，结束view之后
- 会有**response**参数
- 执行顺序与定义顺序相反

```python
@app.after_request
def af1(res):
    print('i am in af1')
    return res

@app.after_request
def af2(res):
    print('i am in af2')
    return res
```

### 3. @app.errorhandler(404)

- 监听状态码只能是 4xx和5xx
- 需要接受错误信息
- 返回值为响应，af会挨个执行

```python
@app.errorhandler(404)
def error404(error_message):
    print(error_message)
    return 'xxx' 		# 5种类型
```

# 3. CBV&session

## 1. CBV

1.  **views.MethodView**：继承让当前class可以成为视图类
2.  定义视图类支持的请求方式
3.  添加路由，as_view(name='login_login')。**name就是endpoint(endpoint=None的情况下)**
4.  可以添加类变量：methods  / decorator = ['is_login']

```python
# CBV
from flask import views
app.add_url_rule('/login', view_func = Login.as_view(name='login_login'))

@app.before_request
def is_login():
  	return 1

@app.after_request
def login_ok(res):
  	return res

# methods：默认是类对应的方法
class Login(views.MethodView):
  	# decorators = []
  	def get(self):
      	return 'here is get.'
    def post(self):
      	pass
```

-   **add_url_rule()：添加路由**

```python
def add_url_rule(self, rule, endpoint=None, view_func=None, **options):pass
# self：flask对象
# rule：路由
# endpoint=None，地址反解析使用，如果为None，则使用view_func的name
# view_func，视图函数，视图类.as_view(name='xxx')
```

-   **view_func()：返回一个 view 函数**

```python
def as_view(cls, name, *class_args, **class_kwargs):pass
# cls：视图类
# name：视图函数名
```

```python
from flask import views
class Index(views.MethodView):
  	def get(self, *args, **kwargs):
      	pass
    ...

app.add_url_rule('/index', endpoint=None, view_func=Login.as_vxwiews(name='login')
```

## 2. redis

### 1. 安装

```python
# win
下载redis到指定目录，配置PATH即可
# mac
brew install redis
```

### 2. 使用

1.  redis使用 key:value 方式存储，**哈希存储结构{key:value}**
2.  多次设置同一个key 会被覆盖

```python
# 终端
redis-cli
# 总共 16 个库，0-15，用来数据隔离
select 8					# 切换 8 号库，默认 0 号库
set key value				# 设置一个健值对，哈希存储结构{key:value}
keys pattern				# 查询当前数据库中所有的key,如keys * 查询当前数据库中所有key
		 a*					# 查询以 a开头
  	 *n*					# 包含 n
...
get key						# 查询 key 对应的 value
```

### 3. python操作redis

1.  --protected-mode no：测试使用，没有设置密码可以使用主机ip
2.   redis只能存储：**byte, string or number**

```python
from redis import Redis
redis_cli = Redis(host='127.0.0.1', port=6379, db=6)
redis_cli.set('name', 'echo')
```

## 3. Flask-session

1.  三方组件：**pip install flask-session**
2.  app.config最终在 **app.default_config**中
3.  settings.py中的DebugConfig中，不是大写英文的一律丢弃不管
4.  使用**pickle**作为序列化器

```python
from flask import Flask, request, session
from flask_session import Session

app = Flask(__name__)
# app.secret_key = '%^&*JBHJ%$*lkdsj'
# 使用 flask_session并使用 redis 存储session
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis('127.0.0.1', 6379, db=10)
Session(app)

@app.route('/sets')
def sets():
  	session['key'] = 'henry'
  	return 'set ok!'
 
@app.route('/gets')
def gets():
  	return session.get('key')

if __name__ == '__main__':
		app.run()
```

-   **flask 利用session_interface，选择session存放位置和机制**

```python
app.session_interface			
# session_interface = self._get_interface(app)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='192.168.12.9', 6379, db=10)
# redis通过pickle序列化，secret_key只有原生的config需要
```

# 4. Flask上下文

-   flask实现线程安全的核心，后期进行详细讲解。

## 1. 偏函数

```python
# flask中的 requst 和 session
from functools import partial

def ab(a, b):
    return a+b

new_func = partial(ab, 1, 3)

print(new_func())
```

## 2. 线程安全

```python
import time
# local：{线程号1:{变量名:值},...}
from threading import local

class Foo(local):
    num = 0
foo = Foo()

def addi(i):
    foo.num = i
    time.sleep(0.2) 		# 相当于 i/o 操作
   	print(foo.num)

from threading import Thread
for i in range(20):
    th = Thread(target=addi, args=(i,))
    th.strat()    
```

## 3.  werkzeug 搭建app

```python
# werkzeug 搭建app
from werkzeug.wrappers import Response, Request
from werkzeug.serving import run_simple

@Request.application
def app(req):
    print(req, req.method)
    return Response('200 ok')

run_simple('0.0.0.0', 5000, app)

# environ：wsgi 处理requset后的结果，请求原始信息
# 对象相当于dict
__slots__ = ('__stroage__', '__ident_func__')
```



## 4. 请求上下文的必要性

1.  当 Flask 应用处理经过 WSGI 处理好的请求数据时，将 `environ` 封装成 request 对象。
2.  为了区分不同请求的请求对象，无非就是只有两种(我只知道两种) 方法，全局变量和使用 Context locals(Werkzeug提供) 实现
3.  很明显Flask请求上下文使用的是第二种方式，当然你可能会有疑问，使用全局变量的方式不是更简单便捷吗？
4.  俗话说得好，一个硬币有两面。使用全局变量可以实现没毛病，那就意味着来多少的请求就需要定义多少个全局变量(细思极恐)，而且我们都知道全局变量在程序中应用时很“危险的”，谁都可以访问，也就会导致数据不安全的情况出现等等等问题。
5.  使用第二种方式就可以完美解决使用全局变量的问题，直到请求处理完毕，Flask 会 pop 掉处理完的请求上下文栈，保证了内存不会溢出。有的同学可能还会提出万一 Flask 应用接收到请求后，服务异常怎么办？Flask 也对此进行进行了相应的处理。

## 5. 源码剖析

**特别说明**

1.  图片中标注的红色数字表示 falsk 应用执行顺序
2.  红色标注代笔请求上文
3.  黄色标注代表请求下文

### 1. 请求上文

-   当请求到来时，Flask 会自动把封装 requst、view functions...的 RequstContext 对象 push 进 Local 对象中
-   当请求数据封装到 environ 后，WSGI 会调用 Flask 实例的 `__call__` 方法，即处理请求

![1 app.__call__](/Users/henry/Documents/截图/Py截图/Flask 请求上文/1 app.__call__.png)

-   我们可以看到，environ 就是请求数据

![2 RequestContext()类](/Users/henry/Documents/截图/Py截图/Flask 请求上文/2 RequestContext()类.png)

-   RequestContext 类实例化时，会对请求数据 environ 进行封装成 request 对象(就是Flask 导入的request)，由app.request_class(environ)，主要是对请求数据的格式化，并初始化request对象
-   我们可以很清晰的看到，request 在 RequestContext 实例化的过程中被封装进对象中了

![3 RequestContext()类-push()](/Users/henry/Documents/截图/Py截图/Flask 请求上文/3 RequestContext()类-push().png)

![4 _requsest_ctx_stack.png](/Users/henry/Documents/截图/Py截图/Flask 请求上文/4 _requsest_ctx_stack.png.png)

![5 LocalStack()类](/Users/henry/Documents/截图/Py截图/Flask 请求上文/5 LocalStack()类.png)

![6 Local()类](/Users/henry/Documents/截图/Py截图/Flask 请求上文/6 Local()类.png)

-   因为在 Local 类中重写了 `__setattr__` 方法，所以在实例化的过程中使用父类的 `__setattr__` 方法

### 2. 请求下文

-   当我们使用 request.method 时，请求下文就开始发挥作用了
-   首先需要导入 `from flask import request`

![4 _requsest_ctx_stack.png](/Users/henry/Documents/截图/Py截图/Flask 请求上文/4 _requsest_ctx_stack.png.png)

-   这里用到了 functools中的 partial() 函数，主要功能有点类似于装饰器，只要参数传递可以分开传递，也就是说可以多次传递，从底层讲可以维护一块内存空间，用于存储变量值
-   可以看到下图类初始化时，使用了`_LocalProxy__local`，这里使用的是私有变量的外部访问方式，私有变量在外部访问不到，本质就是在变量名前加上了 `_类名__私有变量名`的形式。

![7 LocalProxy](/Users/henry/Documents/截图/Py截图/Flask 请求上文/7 LocalProxy.png)

-   当请求处理结束，返回 reponse 给客户端后，Flask通过 信号机制调用`flask.reqeust_tearing_down`和`flask.appcontext_tearing_down`等信号，把当前的request数据销毁，整个请求结束。
  

## 6. Flask 全局变量

-   **`current_app`、`g`、`request`和`session`是`Flask`中常见4个全局变量**。

1.  current_app`是当前`Flask 服务运行的实例
2.  `g`用于在应用上下文期间保存数据的变量
3.  `request`封装了客户端的请求信息
4.  `session`代表了用户会话信息。

## 7. Flask中内置信号

```python
# 模板渲染成功的时候发送，这个信号与模板实例template上下文的字典一起调用。
flask.template_rendered
# 建立请求上下文后，在请求处理开始前发送，订阅者可以用request之类的标准代理访问请求。
flask.request_started
# 在响应发送给客户端之前发送，可以传递reponse。
flask.request_finished
# 在请求处理中抛出异常时发送，异常本身会通过execption传递到订阅函数。
flask.got_request_exception
# 在请求销毁时发送，它总是被调用，即使发生异常。
flask.request_tearing_down
# 在应用上下文销毁时发送，它总是被调用，即使发生异常。
flask.appcontext_tearing_down
```



# 5.websocket

-   使用webscoket实现类似web 微信的一个即时通讯工具
-   流程
    1.  做前端
    2.  建立webserver   django / flask
    3.  制作聊天功能

## 1. 轮询和长链接

### 1. 轮询

-   轮询：只是查询没有超时时间
-   不能保证数据的实时性

```python
# A、B client：无限循环和服务器对话，有 xx 消息吗？
```

-   长轮询：默认有超时时间

```python
# A、B client：client 发起请求至 server，等待15s(默认http超时时间) --> 等待消息时间
# -->主动断开连接
# -->收到消息主动返回
```

### 2. 长链接

-   **短连接**：通讯双方有数据交互时，就建立一个连接，数据发送完成后，则断开此连接，即每次连接只完成一项业务的发送。
-   **长连接**，指在一个连接上可以连续发送多个数据包，在连接保持期间，如果没有数据包发送，需要**双方发链路检测包**。

#### 长连接特性

1.  A、B client --> server 建立连接并保持连接不断开
2.  A to B --> server 消息转发 -->B 建立连接的情况下，可以及时准确收到消息
3.  客户端和服务器保持永久性连接
4.  除非有一方主动发起断开
5.  消息转发

## 2. Websocket 

-   实现的组件：**werkzeug**、**gevent-websocket**

### 1. 示例

-   长连接
-   web + socket
-   Flask + Websocket 模块 + gevent-websocket

```python
# 下载 gevent-websocket，Websocket
# 请求处理 WSGI 处理 HTTP 请求，WebSocketHandler处理socket请求
# 使用 WSGIServer 替换flask的 Werkzueg
# 语法提示
from flask import Flask
from geventwebsocket.hander import WebSocketHandler
from geventwebsocket.server import WSGIServer
from geventwebsocket.websocket import WebSocket

app = Flask(__name__)

@app.route('/ws')
def ichat():
    print(request.environ)
    ws_socket = request.environ.get('wsgi.websocket') # type:WebSocket
    try:
        while True:
            msg = ws_socket.receive()
            print(msg)
            ws_socket.send(b'xxx')
    except:pass
    # return '200 ok!'

if __name__ == '__main__':
    # handler_class=WSGIhandler（not sure），只支持http请求
    http_server = WSGIServer(('0.0.0.0', 9527), app, handler_class=WebSocketHandler)
    http_server.server_forever()
```

### 2. websocket的状态码

-   0：连接创建失败，
-   1：当前link激活，处于可用状态
-   2：客户端主动断开连接，看不到其状态码
-   3：服务器主动发起断开

```js
<script type='application/javascript'>
	var ws = new WebSocket('ws://127.0.0.1:5000/chat');
    ws.onmessage = function (messageEvent) {
        console.log(messageEvent.data);

        var ptag = document.createElement('p');
        ptag.innerText = messageEvent.data;
        document.getElementById('content_list').appendChild(ptag);
    };
    function send_message() {
        var msg = document.getElementById('content').value;
        ws.send(msg);
    }
</script>
// ws.close
```

## 3. websocket

### 1. 单聊示例

1.  群聊时使用 socket_list = []，记录每个连接用户socket_obj
2.  单聊时使用 socket_dict = {}，记录sender 、reciver 和 msg

```python
socket_list = []
@app.route('/chat/<username>')
def chat(username):
    # print(request.environ)
    websocket_obj = request.environ.get('wsgi.websocket')  # type:WebSocket
    websocket_dict[username] = websocket_obj

    while True:
        msg = websocket_obj.receive()

        msg_dict = json.loads(msg)
        receiver = msg_dict.get('receiver')
        try:
            receiver_socket = websocket_dict.get(receiver)

            receiver_socket.send(msg)
        except:
            msg = {'sender': '系统',
                   'receiver': username,
                   'data':'对方不在线',
            }
            websocket_obj.send(json.dumps(msg))


@app.route('/ws')
def ws():
    return render_template('ptop.html')
```

-   ptop.html中的 js

```javascript
<script type="application/javascript">
    var ws;
    function send_message() {
        var msg = {
            sender:document.getElementById('username').value,
            receiver:document.getElementById('receiver').value,
            data:document.getElementById('content').value,
        };

        var data = JSON.stringify(msg);
        ws.send(data);

        var ptag = document.createElement('p');
        ptag.innerText = msg.data + ':' + msg.sender;
        ptag.style.cssText = "text-align:right";
        document.getElementById('content_list').appendChild(ptag);
    }

    function login() {
        var username = document.getElementById('username').value;
        ws = new WebSocket('ws://127.0.0.1:5000/chat/' + username);
        ws.onmessage = function (messageEvent) {
            // 收到信息后先反序列化，在创建 p 标签并加入到div中
            var msg = JSON.parse(messageEvent.data);
            var ptag = document.createElement('p');
            ptag.innerText = msg.sender + ':' + msg.data;
            document.getElementById('content_list').appendChild(ptag);
        };
    }
</script>
```

### 2. 基于websocket实现群聊

1.  建立websocket 服务 + Flask web 框架 + Gevent-WebSocket
2.  requst.environ.get('wsgi.websocket')获取链接，并保存到服务器中
3.  基于长连接socket 接收用户传递的消息
4.  将消息转发给其他用户

### 3. 基于javascirpt 实现websocket客户端

1.  服务器保存的连接方式变化，以dict形式储存
    -   存储结构：{uid: websocket连接, user1:websocket}
2.  消息发送时，receiver， data = {'sender':发送方, 'receiver':接收发, data:数据}
    -   从data中找到接收方的key
    -   去存储结构中找到 key 对应的websocket连接
3.  websocket.send(data).  socket传输， bytes类型
4.  js 中常用的事件

```javascript
var ws = new WebSocket('ws://ip:port/路径')
// ws.onmessage 当ws客户端收到消息时执行回调函数
// ws.onopen 当ws客户端建立完成连接时， status == 1 时执行
// ws.onclose 当ws客户端关闭中后关闭，执行的回调函数，status 2 或 3
// ws.onerror 当ws客户端出现错误时
ws.onmessage = func(messageEvent){
    ...
}
```

## 4. 示例

```python
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
    print('建立app_socket连接。。。', app_socket, user_id)
    while True:
        try:
            # 收发数据
            msg = app_socket.receive()
            msg_info = json.loads(msg)
            receiver = msg_info.get('to_user')
            receiver_socket = web_socket.get(receiver)
            try:
            	receiver_socket.send(msg)
            except:
                web_socket.pop(receiver)
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
```

## DButils模块：数据库连接池

# 6. SQLAlchemy

-   通用的ORM框架
-   Django-Model：基于django

## 1. 安装

```python
pip install sqlalchemy
```

## 2. 使用

### 0. 基本流程

#### 1. models类的创建(6)

1.  声明一个基类：`from sqlalchemy.ext.declarative import declarative_base`

2.  实例化基类：`BaseModel = declarative_base()`

3.  创建model类：

    ```python
    from sqlalchemy import INT, String, Column
    class Test(BaseModel):
        __tablename__ = 'test'
        id = Column(INT, primary_key=True)
        name = Column(String(32), nullable=False, index=True, unique=True)
    ```

4.  创建数据库引擎：`from sqlalchemy.engine import create_engine`

5.  连接数据库：

    -   `engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/sqlalchemy?charset=utf8')`

6.  创建表：`BaseModel.metadata.create_all(engine)`

#### 2. 操作数据库(4)

1.  创建查询窗口：`from sqlalchemy.orm import sessionmaker`
2.  选择数据库：`db_select = sessionmaker(engine)`
3.  打开查询窗口：`db_session = db_select()`
4.  CRUD操作：本质是ORM操作
    -   `db_session.add(User('henry')) / commit() / close()`
    -   `db_session.add_all(user_list)`

### 1. 约束

1.  primary_key
2.  auto_increment
3.  nullable
4.  index
5.  unique

### 2. 数据类型

-   INT、INTEGER、Integer：都是整型
-    CHAR、 NCHAR、VARCHAR、 NVARCHAR、String：都是字符串

```python
# 声明一个基类，相当于 models 类
from sqlalchemy.ext.declarative import declarative_base
BaseModel = declarative_base()

from sqlalchemy import Column, INT, String
# ORM：object relationship mapping
class User(BaseModel):
    # 创建一个table
    __tablename__ = 'user'
    id = Column(INT, primary_key=True, auto_increment=True)
    name = Column(String(32), nullable=False, index=True, unique=True)
  
# 数据库引擎创建
from sqlalchemy.engine import create_engine
# 数据库连接驱动语句
engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/sqlalchemy?charset=utf8')

# 利用 User 去数据库创建 user Table
BaseModel.metadata.create_all(engine)
```

-   增加数据

```python
# 1. 选择数据库
from sqlalchemy.engine import create_engine
engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/sqlalchemy?charset=utf8')
from sqlalchemy_study import engine
# 2. 选择表
from sqlalchemy_study import User
# 3. 创建查询窗口
from sqlalachemy.orm import sessionmaker
# 选中数据库
select_db = sessionmaker(engine)
# 已经打开查询窗口
db_session = select_db()
```

-   插入、批量插入，add、add_all

```python
# 1. 写入sql语句
user = User(name='henry')
db_session.add(user)
# 批量创建
user_list = [User(name=i) for i in ['henry', 'echo', 'dean'...]]
db_session.add_all(user_list)
# 2. 提交sql
db_session.commit()
# 3. 关闭窗口
db_session.close()
```

-   查询，query

```python
# 查询所有数据
res = db_session.query(User).all()
print(res[0].id, res[0].name)
# 查询第一条数据
res = db_session.query(User).first()
print(res.id, res.name)

# 查询id=3的数据，数据是list
res = db_session.query(User).filter(User.id==3, User.name=='123').all()
or 
res = db_session.query(User).filter_by(id=3, name='123').all()
print(res[0].id, res[0].name)
```

-   修改，update

```python
# 修改数据
db.session.query(User).filter(User.id==1).update({'name':'dean'})
db_session.commit()
db_session.close()
```

-   删除数据，delete

```python
# 删除数据
db.session.query(User).filter(User.id==1).delete()
db_session.commit()
db_session.close()
```

## 3. 外键

### 1. 创建表

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.engine import create_engine
# 几乎支持所有的关系型数据库
engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/sqlalchemy?chrset=utf8')
BaseModel = declarative_base()
```

-   **一对多的关系**：外键
    -   ` sch_id = Column(Integer, ForeignKey('shool.id'))` 
    -   `stu2sch = relationship('School', backref='sch2stu')`

```python
# ORM 精髓, relationship 所在的类是正向类
from sqlalchemy.orm imoprt relationship
class School(BaseModel):
    __tablename__ = 'school'
    # auto_increment可以省略
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

class Student(BaseModel):
    __tablename__ = 'studnet'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    sch_id = Column(Integer, ForeignKey('shool.id'))
	# mapping
    stu2sch = relationship('School', backref='sch2stu')

BaseModel.metadata.create_all(engine)
```

### 2. 操作

```python
from sqlalchemy.orm import sessionmaker
from xxx import engine
select_db = sessionmaker(engine)
db_session = select_db()
```

#### 1. 增加

```python
# 1. 创建一个学校、查询其id，利用id再去创建学生添加 sch_id
# 2. relastionship 正向添加，字段出现在哪个类
from xxx import Student, School
stu = Student(name='iris', stu2sch=School(name='BeiJing'))
db_session.add(stu)
db_session.commit()
db_seesion.close()
# 3. relastionship 反向添加
sch = School(name='Shanghai')
sch.sch2stu = [Student(name='henry'), Student(name='echo')]
db_session.add(sch)
db_session.commit()
db_session.close()
```

#### 2. 删除

-   当前学校被引用的时候不可以删除

#### 3. 查询

```python
# 正向查询
res = db_session.query(Student).all()
print([(stu.name, stu.stu2sch.name) for stu in res])
# 反向查询
res = db_session.query(School).all()
print([(sch.name, len(sch.sch2stu)) for sch in res])
print([(sch.name, [stu.name for stu in sch.sch2stu]) for sch in res])
```

## 4. ManyToMany

-   获取到多个对象类型为：`<class 'sqlalchemy.orm.collections.InstrumentedList'>`

### 1. 创建表

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import relationship
# 几乎支持所有的关系型数据库
engine=create_engine('mysql+pymysql://root:root@127.0.0.1:3306/sqlalchemy?chrset=utf8')
BaseModel = declarative_base()bd
```

-   多对多表

```python
class Girl(BaseModel):
    __tablename__ = 'girl'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    # 注意secondary是表层面的
    gyb = relationship('Boy', backref='byg', secondary='hotel')

class Boy(BaseModel):
    __tablename__ = 'boy'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

class Hotel(BaseModel):
    __tablename__ = 'hotel'
    id = Column(Integer, primary_key=True)
    bid = Column(Integer, ForeignKey('boy.id'))
    gid = Column(Integer, ForeignKey('girl.id')) 

BaseModel.metadata.create_all(engine)
```

### 2. 操作

-   **第三张表的数据是自动添加的**

```python
from sqlalchemy.orm import sessionmaker
from xxx import engine, Girl, Boy
select_db = sessionmaker(engine)
db_session = select_db()
```

#### 1. 增加

```python
# 使用relationship正向增加
g = Girl(name='echo', gyb=[Boy(name='ehco1'),Boy(name='echo2')])
db_session.add(g)
db_session.commit()
db_sesion.close()

# 反向添加
b = Boy(name='dean')
b.byg = [
    Girl(name='dean1'),  
    Girl(name='dean2')
        ]
db_sesion.add(b)
db_session.commit()
db_sesion.close()
```

#### 2. 查询

-   查询结果必须使用 .all() 或者 .first()

```python
# 正向查询
res = db_session.query(Girl).all()
for g in res:
    print(g.name, len(g.gyb))
    
# 反向查询
res = db_session.query(Boy).all()
for b in res:
    print(b.name, len(b.byg))
```

## 5. 小结

### 1.  filter和filter_by

```python
query = db_session.query(User)
# 等于判断
query.filter(User.name =='test') 								# equals
query.filter(User.name !='test') 								# not equals
# 模糊匹配
query.filter(User.name.like('%es%')) 							# like 模糊匹配
# 成员判断
query.filter(User.name.in_(['test','henry', 'echo'])) 			# in 成员判断
query.filter(~User.name.in_(['test','henry', 'echo']))			# not IN
query.filter(User.name.in_(session.query(User.name).filter(User.name.like('%ed%'))	# IN
# None判断
query.filter(User.name ==None)									# is None
query.filter(User.name !=None)									# not None

# 多条件判断，逻辑与         
from sqlalchemy import and_
query.filter(and_(User.name =='test', User.age ==18)) 			# and
query.filter(User.name =='test', User.age ==18) 				# and
query.filter(User.name =='test').filter(User.age ==18)			# and
# 逻辑或
from sqlalchemy import or_
query.filter(or_(User.name =='test', User.age ==18)) 			# or
# 匹配
query.filter(User.name.match('test'))							# match
```

### 2. 查询的方式

-   `func`为内置函数

```python
from sqlalchemy import func
# sql过滤
print(session.query(User).filter("id>:id").params(id=1).all())

# 关联查询 
print(session.query(User, Address).filter(User.id == Address.user_id).all())
print(session.query(User).join(User.addresses).all())
print(session.query(User).outerjoin(User.addresses).all())

# 聚合查询
print(session.query(User.name, func.count('*').label("user_count")).group_by(User.name).all())
print(session.query(User.name, func.sum(User.id).label("user_id_sum")).group_by(User.name).all())

# 子查询
stmt = session.query(Address.user_id, func.count('*').label("address_count")).group_by(Address.user_id).subquery()
print(session.query(User, stmt.c.address_count).outerjoin((stmt, User.id == stmt.c.user_id)).order_by(User.id).all())

# exists
print(session.query(User).filter(exists().where(Address.user_id == User.id)))
print(session.query(User).filter(User.addresses.any()))

# count distinct "name" values
from sqlalchemy import distinct
session.query(func.count(distinct(User.name)))
```

## 6. 执行原生SQL

```python
"""执行原生SQL"""
from sqlalchemy import create_engine
db = create_engine('mysql+pymysql://root:root@localhost:3306/sqlalchemy?charset=utf8')
conn = db.connect()
conn.execute("insert into user(name, age) values('iris', 18)")
res = conn.execute('select * from user')
print(list(res))
```



# 7.Flask-SQLAlchemy

## 1. 安装

```python
pip install flask-sqlalchemy
```

## 2. flask项目结构

### 1. app01包

-   templates：文件夹
-   static：文件夹
-   `__init__.py`

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
# 创建 db 时，注意导入蓝图的顺序
from views import user

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/sqlalchemy?charset=utf8'
    # 一般小于50，默认不开启
    app.config['SQLALCHEMY_POOL_SIZE'] = 5
    # 默认是 15s
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 15
    # 每个链接重复使用次数，一般不写
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 10
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.register_blueprint(user.users)
    # 读取 config 文件
    db.init_app(app=app)
    return app
```

-   models.py

```python
# db是 sqlalchemy 对象
from app01 import db

# db.Model 就是 BaseModel，使用的是sqlalchemy
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

if __name__ == '__main__':
    from app01 import create_app
    app = create_app()
    db.drop_all(app=app)
    db.create_all(app=app)
```

-   views：存放蓝图文件夹
    -   user.py

```python
from flask import Buleprint
from app01.models import db, Users
user = Blueprint('user', __name__)

@user.route('/reg/<username>')
def reg(username):
    u = Users(name=username)
    db.session.add(u)
    db.sessoin.commit()
    return 'reg 200 OK!'  

@user.route('/user_list')
def user_list():
    res = Users.query.filter('条件').all()
    print(res)
    return f'当前有{len(res)}个用户。'
```

### 2. manager.py

```python
from app01 import create_appf
app = create_app()
if __name__ == '__main__':
    app.run()
```

### 3. 使用流程

#### 1. 实例化db

`db = SQLAlchemy()`

#### 2. app配置

```python
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/sqlalchemy1?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 注册蓝图
app.register_blueprint(user.user)
```

#### 3. 初始化db

`db.init_app(app=app)`

#### 4. Migrate

`Migrate(app, db)`

#### 5. Manager

-   `manager = Manager(app)`
-   `manager.add_command('db', MigrateCommand)`
-   ``



## 3. 终端启动

### 1. 下载

```python
pip install flask-script
```

### 2. 使用

-   manager.py

```python
from app01 import create_app
from flask_script import Manager
app = create_app()
manager = Manager(app)
"""
# 进阶
@manager.command
def func1(args):
    print(args)
   	return args
   	
@manager.option('-w', '--who', dest='who')
@manager.option('-a', '--age', dest='age')
def func(who, age):
    print(who, age)
   	return who, age
"""

if __name__ == '__main__':
    manager.run()
```

-   终端命令

```python
# 此时注意当前的 python 解释器
python manager.py runserver -h 0.0.0.0 -p 9527
```

-   **指令集**

```python
# func1 函数传参
python manager.py func1 haha
# 多重传参
python manager.py -w henry
python manager.py -w henry -s echo
```

### 3. flask-migrate

-   **如果使用，必须安装flask-script**

```python
from app01 import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
app = create_app()
Migrate(app, db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
```

-   终端使用

```python
# 初始化数据库，会清空数据库
python manager.py db init
# 相当于Django的makemigrations
python manager.py db migrate
# 相当于Django的migrate
python manager.py db upgrade
```