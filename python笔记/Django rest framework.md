### 开发模式

#### 1. 普通开发模式

-   前后端一起写

#### 2. 前后端分离优势

1.  开发效率高，后端代码只用一套就可以了
2.  数据源只有一套，前端可以有多套，适用于多种终端

#### 3. 后端开发

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

### 3. 示例

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

## 2. 权限

  

## 3. 节流(访问频率)



## 4. 版本



















