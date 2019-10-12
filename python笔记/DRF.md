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
            self.initial(request, *args, **kwargs)
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
2. 执行 self.initialize_request(request, *args, **kwargs)
3. 执行 self.initial(request, *args, **kwargs)
4. 执行 initial 中的 self.perform_authentication(request)
5. 即：request.user
6.  @property
    def user(self):
        ...
        self._authenticate()
7. 执行 _authenticate(self)，循环 self.authenticators 对象，执行 authenticate 的方法
8. 执行自定义类中的 authenticate 的方法
9. 执行视图函数
```

### 6. 匿名用户配置

-   推荐`UNAUTHENTICATED_USER`:为None，token也为 None
-   DEFAULT_AUTHENTICATION_CLASSES：自定义**默认验证的类**，全局使用
-   如果要某个类免除认证，**则添加`authentication_classes = []`即可**
-   **配置全局有效**

```python
REST_FRAMEWORK = {
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
    # 认证相关
    'DEFAULT_AUTHENTICATION_CLASSES': ['app01.utils.auth.MyAuth'],
    'UNAUTHENTICATED_USER': lambda: '匿名用户',
    'UNAUTHENTICATED_TOKEN': lambda: '匿名用户的token',
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
    'DEFAULT_AUTHENTICATION_CLASSES': ['app01.utils.auth.MyAuth'],
    # 'DEFAULT_AUTHENTICATION_CLASSES': [],
    'UNAUTHENTICATED_USER': None,
    'UNAUTHENTICATED_TOKEN': None,
	# 权限
    'DEFAULT_PERMISSION_CLASSES': ['app01.utils.Permissions.MyPermission'],
    # 节流
    'DEFAULT_THROTTLE_CLASSES': ['app01.utils.MyThrottle.UserThrottle'],
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

## 5. 解析器*

## 6. 序列化器****

## 7. 分页**

## 8. 路由**

## 9. 视图**

## 10. 渲染器*

















