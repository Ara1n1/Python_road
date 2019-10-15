# 开发模式

1.  普通开发模式
    -   前后端一起写
2.  前后端分离优势
    1.  开发效率高，后端代码只用一套就可以了
    2.  数据源只有一套，前端可以有多套，适用于多种终端
3.   后端开发
    1.  API开发
    2.  返回HttpResponse

# restful

## 0. 安装模块

```python
pip install djangorestframework
```

## 1. 基于CBV的认证

### 1. APIView.dispatch方法

-   **dispatch 是 request 请求的入口**

1.  对原生的 request 进行加工（**丰富了一些功能**），封装了 request 和 Basic对象list
2.  获取**原生的 request**，使用 `request._request`
3.  获取**认证类对象**，`request.authenticators`


```python
import json
from django.shortcuts import HttpResponse
from rest_framework import exceptions
from rest_framework.views import APIView

class MyAuthentication(object):
    
    def authenticate(self, request):
        # 这里可以获取用户名和密码，用来认证
        token = request._request.GET.get('token')
        if not token:
            # 认证失败抛异常
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 认证成功返回一个元组
        return ('henry', None)
    
    def authenticate_header(self, request):
        pass

class Test(APIView):
    authentication_classes = [MyAuthentication, ]

    def get(self, request):
        print(request)
        return HttpResponse(json.dumps({'status': '200 ok', 'name': 'henry'}))

    def post(self, request):
        return HttpResponse('POST')
```

### 2. 代码的流程

#### 1. dispatch执行流程

1.  `request = self.initialize_request(request, *args, **kwargs)`
    -   此时的 request 封装了原生的 **requst** 和 **authenticators**
    -   request 本质是 Request 对象
    -   authenticators=self.get_authenticators()
2.  `self.initial(request, *args, **kwargs)`
    -   Runs anything that needs to occur prior to calling the method handler.
    -   实现：**认证、权限、节流、版本**等功能
    -   如：`self.perform_authentication(request)`

#### 2. 源码解读

1.  获取原生的 request ：request._request
2.  获取认证类对象：request.authenticators 

```python
# Provides an APIView class that is the base of all views in REST framework
class APIView(View):
    def dispatch(self, request, *args, **kwargs):
      	...
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        ...
        try:
            self.initial(request, *args, **kwargs)   # 执行 用户、权限、节流 功能
            # 此时的 request 是封装后的，.method 调用的是 __getattr__ 方法
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            response = handler(request, *args, **kwargs)
        except Exception as exc:
            response = self.handle_exception(exc)
        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response
    
    def get_authenticators(self):
        return [auth() for auth in self.authentication_classes]
    # self.initial(request, *args, **kwargs)中调用
    def perform_authentication(self, request):
        request.user
```

### 3. 登录

```python
from rest_framework.views import APIView
from django.http import JsonResponse

def md5(user):
    import hashlib, time
    m = hashlib.md5(bytes(user, encoding='utf8'))
    m.update(bytes(str(time.time()), encoding='utf8'))
    return m.hexdigest()

class AuthView(APIView):

    def post(self, request):
        ret = {'code': 1000, 'msg': None}
        user = request._request.POST.get('username')
        pwd = request._request.POST.get('password')
        obj = models.UserInfo.objects.filter(username=user, password=pwd)
        if not obj:
            ret['code'] = 1001
            ret['msg'] = '用户名或密码错误'
        else:
            # 为登录用户创建 token
            token = md5(user)
            # token 存在更新，不存在更新
            user_id = obj.first().id
models.UserToken.objects.update_or_create(user_id=user_id, defaults={"token": token})
            ret['token'] = token
        return JsonResponse(ret)
```

### 4. 认证访问

1.  `request.user `和` request.auth `**分别是验证类执行方法时返回的元组**
2.  如果验证类，没有返回值则交由下一个验证类进行处理，如果**都没有返回值**，则使用默认值：即**AnonymousUser**
3.  如果是异常则抛：`raise exceptions.AuthenticationFailed(ret)`
4.  **认证一般不加多个**

```python
data = {
    1: {'name': 'henry'},
    2: {'name': 'echo'},
}
class MyAuth:
	
    def authenticate(self, request):
        ret = {'code': 1000, 'msg': None, 'data': None}
        token = request.GET.get('token')
        models.UserToken.objects.filter(token=token).first()
        if not token:
            ret['code'] = 1001
            ret['msg'] = '用户没有登录'
            raise exceptions.AuthenticationFailed(ret)
        # restful framework 内部会赋值给requst，供以后使用
        return token.user, token
    # 认证失败时，返回给浏览器的响应头
    def authenticate_header(self, request):
        pass

class OrderView(APIView):
    # 需要认证的加上即可
    authentication_classes = [MyAuth, ]
    
    def get(self, request):

        ret = {'code': 1000, 'msg': None, 'data': None}
        try:
            ret['data'] = data
        except exceptions as e:
            pass
        return JsonResponse(ret)
```

### 5. 认证的执行流程

```python
# apiview
1. 执行dispatch()
2. 执行 self.initialize_request(request, *args, **kwargs)，封装了所有的认证类
3. 执行 self.initial(request, *args, **kwargs)
4. 执行 initial 中的 self.perform_authentication(request)执行request.user
6. @property
   def user(self):
       ...
       self._authenticate()
7. 执行 _authenticate(self)，循环 self.authenticators 对象，执行 authenticate 的方法
8. 执行自定义类中的 authenticate 的方法
9. 执行视图函数
```

### 6. 匿名用户配置

-   推荐`UNAUTHENTICATED_USER`：**为None，token也为 None**
-   DEFAULT_AUTHENTICATION_CLASSES：自定义**默认验证的类**，全局使用
-   如果要某个类免除认证，**则添加`authentication_classes = []`即可**
-   **配置全局有效**

```python
REST_FRAMEWORK = {
    # 认证
    'DEFAULT_AUTHENTICATION_CLASSES': ['app01.utils.auth.MyAuth'],
    'UNAUTHENTICATED_USER': lambda: '匿名用户',
    'UNAUTHENTICATED_TOKEN': lambda: '匿名用户的token',
}
```

### 7. 内置的认证类

#### 1. 内置类的用法

-   为了规范认证类的写法，**通常我们都继承 BaseAuthentication** 类
-   **必须实现类中的两个方法**

```python
from rest_framework.authentication import BaseAuthentication

# 自定义的认证类
class MyAuth(BaseAuthentication):
    def authenticate(self, request):
        ret = {'code': 1000, 'msg': None, 'data': None}
        token = request.GET.get('token')
        models.UserToken.objects.filter(token=token).first()
        if not token:
            ret['code'] = 1001
            ret['msg'] = '用户没有登录'
            raise exceptions.AuthenticationFailed(ret)
        # restful framework 内部会赋值给requst，供以后使用
        return token.user, token
    # 认证失败时，返回给浏览器的响应头
    def authenticate_header(self, request):
        pass
```

#### 2. BasicAuthentication

-   跳出的用户名和密码如：FTP，**浏览器提供的功能**
-   用户名和密码放在请求头中，**会加密**
-   一种公认的认证方式

## 2. 权限

### 1. 基本使用

```python
class MyPermission():
    # 没有权限的提示信息
    message = 'xxxx'
    def has_permission(self, request, view):
        # 返回 True 则有权访问
        return False
          
class OrderView(APIView):
    # 需要认证的加上即可
    authentication_classes = [MyAuth, ]
    # 返回 True 有权访问
    permission_classes = [MyPermission,]
    def get(self, request):
		pass
```

### 2. 配置文件

```python
REST_FRAMEWORK = {
    # 权限相关
    'DEFAULT_PERMISSION_CLASSES': ['app01.utils.Permissions.MyPermission']
}
```

### 3. 内置权限类

-   为了规范认证类的写法，**通常我们都继承 BasePermission** 类
-   返回True表示有权访问，False 表示无权访问，可以抛异常

```python
from rest_framework.permissions import BasePermission

# 自定义的权限类
class MyPermission(BasePermission):
    # 没有权限的提示信息
    message = 'xxxx'
    def has_permission(self, request, view):
        # 返回 True 则有权访问
        return False
```

## 3. 节流(访问频率)

### 1. 访问频率限制

#### 1. 不继承BaseThrottle

```python
import time

class MyThrottle(object):
    VISIT_HIS = {}

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        atime = time.time()
        remote_addr = request.META.get('REMOTE_ADDR')
        self.history = self.VISIT_HIS.get(remote_addr)
        if not self.history:
            self.VISIT_HIS[remote_addr] = [atime, ]
            return True
        while self.history and self.history[-1] < atime - 10:
            self.history.pop()
        if len(self.history) < 3:
            self.history.insert(0, atime)
            return True

    def wait(self):
        return 10 - time.time() + self.history[-1]
```

#### 2. 继承BaseThrottle

```python
import time
from rest_framework.throttling import BaseThrottle
class MyThrottle(BaseThrottle):
    VISIT_HIS = {}

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        atime = time.time()
        remote_addr = self.get_ident(request)
        self.history = self.VISIT_HIS.get(remote_addr)
        if not self.history:
            self.VISIT_HIS[remote_addr] = [atime, ]
            return True
        while self.history and self.history[-1] < atime - 10:
            self.history.pop()
        if len(self.history) < 3:
            self.history.insert(0, atime)
            return True

    def wait(self):
        return 10 - time.time() + self.history[-1]
```

#### 3. 继承SimpleRateThrottle

```python
from rest_framework.throttling import SimpleRateThrottle
# 针对匿名用户，使用 ip 地址作为标识
class MyThrottle(SimpleRateThrottle):
    scope = 'any string'

    def get_cache_key(self, request, view):
        return self.get_ident(request)

# 针对登录用户
class UserThrottle(SimpleRateThrottle):
    scope = 'user'

    def get_cache_key(self, request, view):
        return request.user.username
```

### 2. 配置文件

```python
REST_FRAMEWORK = {
    # 认证
    'DEFAULT_AUTHENTICATION_CLASSES': ['app01.utils.Auth.MyAuth'],
    'UNAUTHENTICATED_USER': None,
    'UNAUTHENTICATED_TOKEN': None,
	# 权限
    'DEFAULT_PERMISSION_CLASSES': ['app01.utils.Permissions.MyPermission'],
    # 节流
    'DEFAULT_THROTTLE_CLASSES': ['app01.utils.Throttle.UserThrottle'],
	# 设置 scope
    'DEFAULT_THROTTLE_RATES': {
        'any string': '3/m',
        'user':'10/m',
    }
}
```

### 3. 使用方式

#### 1. 局部使用

```python
class 类():	
    authentication_classes = [MyAuth,]
    permission_classes = [MyPermission,]
    throttle_classes = [MyThrottle, ]
    def ...
```

#### 2. 全局使用

-   使用配置文件

## 4. 版本*

### 1. 版本

-   restful规定放置于：url 或者 请求头中

### 2. 版本获取

-   版本号在**URL**中：`http://127.0.0.1:8000/api/users/?version=v1`

#### 1. 自定义获取版本号

```python
class ParamVersion:
    def determine_version(self, request, *args, **kwargs):
        # reqeust.query_params.get('version')等价于 request._request.GET.get('version')
        version = request.query_params.get('version')
        return version

class UserView(APIView):
    versioning_class = ParamVersion

    def get(self, request, *args, **kwargs):
        print(request.version)
        return HttpResponse('用户列表')
```

#### 2. 使用内置的类

-   通过 versioning_class **表示局部使用**
-   一般通过配置文件进行全局配置，只要配置一份即可

```python
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning
class UserView(APIView):
    # 版本：http://127.0.0.1:8000/api/users/?version=1
    # versioning_class = QueryParameterVersioning
    
    # 版本：http://127.0.0.1:8000/api/v1/users/
    # versioning_class = URLPathVersioning
     
    # 通过类获取 版本
    print(request.version)
    # url 方向解析
    url = request.versioning_scheme.reverse(viewname='user', request=request)
    print(url, 'here')
    # 使用django 的url 反向解析
    user_url = reverse(viewname='user', kwargs={'version': 'v2'})
    print('user_url: ', user_url)
    return HttpResponse('用户列表')
```

-   路由系统

```python
# 项目的 url
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^api/', include('app01.urls')),
]

# app01
from django.conf.urls import url
from app01 import views
urlpatterns = [
    url(r'^(?P<version>[v1|v2]+)/users/$', views.UserView.as_view(), name='user'),
]
```

-   配置文件

```python
REST_FRAMEWORK = {
    # 设置获取版本的类，这里使用 URLPathVersioning
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'VERSION_PARAM': 'version',
}
```

### 3. 源码获取版本流程

-   完整的 **intial** 方法

```python
class APIView(View):
	def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)
        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted
        # 认证相关
        self.perform_authentication(request)
        # 权限相关
        self.check_permissions(request)
        # 节流相关
        self.check_throttles(request)
    
    # 获取
	def determine_version(self, request, *args, **kwargs):
        if self.versioning_class is None:
            return (None, None)
        scheme = self.versioning_class()
        # 执行version类中的 determine_version 方法，和 version类的对象
        return (scheme.determine_version(request, *args, **kwargs), scheme)
```

## 5. 解析器*

### 1. django的request.POST和body

#### 1. reqeust.POST有值的条件

1.  如果请求头要求：`Content-Type:applicatoin/x-www-form-urlencode`，request.POST 才有值（request.body中解析数据）
    -   form表单默认提交的数据请求头
    -   ajax默认的请求头也符合这个要求
2.  数据格式要求：`name=henry&pwd=123`

#### 2. POST中没有值

-   可以从body中获取

```python
# 此时 request.POST中没有值，但可以从 request.body 中获取
$.ajax({
    url:...,
    type:'POST',
    # 此时 request.POST中没有值
    headers:{Content-Type:'applicatoin/json',},
    # data 内部会转换为 name=henry&pwd=123 格式
    data:{
        name:'henry',
        pwd:123,
    }
})
```

### 2. resful_framework解析器

-   使用时全局配置
-   使用：request.data 取值时会触发解析

#### 1. 可以发json数据

-   支持请求头：`content-type:'applicatoin/json'`
-   支持数据：{'name': 'henry', 'pwd': 123}
-   获取数据：`reu`

```python
from rest_framework.parsers import JSONParser

class ParserView(APIView):
    """
    JSONParser 表示只能解析：Content-Type:applicatoin/json 的数据
    FormParser 表示只能解析：Content-Type:applicatoin/x-www-form-urlencode 的数据
    """
    parser_classes = [JSONParser, FormParser]

    def post(self, request, *args, **kwargs):
        # 获取解析后的结果
        print(request.POST)
        # print(request.body)
        print(request.data)
        return HttpResponse('ParserView')
```

#### 2. 处理流程

1.  获取用户请求
2.  获取用户请求体
3.  根据请求头和 解析器支持的请求头进行比较，然后解析
4.  request.data

#### 3. 配置文件

-   settings.py

```python
REST_FRAMEWORK = {
    # 设置获取版本的类，这里使用 URLPathVersioning
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'VERSION_PARAM': 'version',
    # 设置使用的解析器
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser', 
        'rest_framework.parsers.FormParser'
    ]
}
```

### 3. 源码流程 

-   本质：根据**content-type**头进行数据解析

```python
1. 执行 request.data
	@property
	def data(self):
    	if not _hasattr(self, '_full_data'):
            self._load_data_and_files()
            return self._full_data
2. 调用 _load_data_and_files() 方法，执行  self._parse()
3. 执行选择 parser = self.negotiator.select_parser(self, self.parsers)，解析器
4. 调用解析器类parser对象的 parse 方法
	parsed = parser.parse(stream, media_type, self.parser_context)
5. 返回解析好的数据
```

## 6. 序列化****

## 7. 分页**

## 8. 路由**

## 9. 视图**

## 10. 渲染器*

















