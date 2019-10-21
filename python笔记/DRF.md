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

1.  如果请求头要求：`Content-Type:applicatoin/x-www-form-urlencode`，和请求数据格式必须是`key:value & key :value...`的格式，request.POST 才有值（request.body中解析数据）
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

## 6. 序列化`****`

### 1. 功能

1.  请求数据的验证
2.  queryset进行序列化  

### 2. 序列化器类

-   **models类**

```python
from django.db import models

class UserGroup(models.Model):
    title = models.CharField(max_length=32)

class UserInfo(models.Model):
    user_type_choices = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP'),
    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
	# 外键和多对多关系
    group = models.ForeignKey('UserGroup')
    role = models.ManyToManyField('Role')

class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo')
    token = models.CharField(max_length=64)

class Role(models.Model):
    title = models.CharField(max_length=32)
```

#### 1. 简单使用

-   ser.data：表示序列化后的数据，ser是序列化器对象

```python
"""序列化器"""
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=32)

# 视图类
class RoleView(APIView):
    def get(self, request, *args, **kwargs):
        roles = models.Role.objects.all()
        # 方式一
        # roles = roles.values()
        # print(type(roles), roles)
        # roles = json.dumps(list(roles), ensure_ascii=False)

        # 方式二，针对多个对象，如果是单个对象则 many=False
        ser = MySerializer(instance=roles, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)

        return HttpResponse(ret)
```

#### 2. 特殊字段

-   choices、外键、多对多关系
-   **多对多关系**：需要自定义方法，返回值为页面显示内容
-   RoleView视图类同上

```python
"""序列化器"""
class UserInfoSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # choices 选项
    user_type = serializers.CharField(source='get_user_type_display')
    # 外键
    group = serializers.CharField(source='group.title')
    # 多对对关系，自定义显示
    role = serializers.SerializerMethodField()

    # 自定义方法
    def get_role(self, row):
        row_obj_list = row.role.all()
        ret = []
        for i in row_obj_list:
            ret.append({'id': i.id, 'title': i.title})
        return ret
```

#### 3. 继承ModelSerializer

```python
"""序列化器"""
class UserInfoSerializer(serializers.ModelSerializer):
    # 增加其他字段，如果字段名和 model 类中相同，则覆盖
    group = serializers.CharField(source='group.title')
    user_type = serializers.CharField(source='get_user_type_display')

    class Meta:
        model = models.UserInfo
        fields = '__all__'
        # 表示深入到第几层，设置后不用重写 多对多和外键字段，建议 1-10
        depth = 1
```

#### 4. 自定义字段类

```python
# 自定义字段类
class MyField(serializers.CharField):
    def to_presentation(self, value):
        print(value)
        return 'xxx'

class UserInfoSerializer(serializers.ModelSerializer):
    # 增加其他字段，如果字段名和 model 类中相同，则覆盖
    group = serializers.CharField(source='group.title')
    
    # 生称 url，lookup_url_kwarg 是 url 中的参数
    # group = serializers.HyperlinkedIdentityField(view_name='gp', lookup_field='group_id', lookup_url_kwarg='pk')
    user_type = serializers.CharField(source='get_user_type_display')
    # 自定义字段
    xxx = MyField()
    class Meta:
        model = models.UserInfo
        fields = '__all__'
```

### 3. 生成hypermedialink

#### 1. 返回hypermedialink

-   查看group时，使用 url
-   `lookup_field='group_id'`：表示被序列化**数据表中**的字段，`lookup_url_kwarg`是 url 中的参数
-    `serializer`**实例化**：必须加上 `context={'request': request}` 参数

```python
 class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserGroup
        fields = '__all__'

class GroupView(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        groups = models.UserGroup.objects.filter(pk=pk)
        # 必须加上 context 参数
        ser = UserInfoSerializer(instance=userinfo, many=True, context={'request': request})
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)
```

#### 2. url.py 配置

```python
urlpatterns = [
	...
	url(r'^(?P<version>[v1|v2]+)/group/(?P<pk>\d+)$', views.GroupView.as_view(), name='gp'),
]
```

### 4. 结论

1.  使用rest_framework提供的序列化器：先导入
2.  创建**自定义的序列化类**，如果不指定`source='字段名'`，属性名称必须为数据库中的字段名
3.  **choices选项的字段**：指定`soucre=get_字段名_display`，本质是通过通过执行函数获取，**内部会判断**(如果是可调用的则直接调用，不可调用的则直接返回)，这里**不需要加括号**
4.  **多对多关系**：使用` xxx = serializers.SerializerMethodField()`，自定义显示，定义函数名为 `get_xxx(self, row)`
5.  继承 `ModelSerializer`类时，只要使用了 `depth = 1`，自动化序列化，连表获取 `多对多或外键 `的数据
6.  生成连接：`group = serializers.HyperlinkedIdentityField(view_name='gp', lookup_field='group_id', lookup_url_kwarg='pk')`

### 5. 源码流程

1.  对象：交由 `Serializer`处理，如果是 `QuerySet`交由`ListSerializer`处理
2.   `ser.data`˙中调用：`self.representation`

### 6. 请求数据校验

#### 1. 验证post数据

-   使用postman提交数据，如过没有任何数据则会输出
    -   `{'title': [ErrorDetail(string='标题字段不能为空', code='required')]}`
-   有数据：`OrderedDict([('title', 'test')])`

```python
"""验证功能"""
# 自定义验证规则
class XxValidator(object):

    def __init__(self, base):
        self.base = base

    def __call__(self, value, *args, **kwargs):
        if not value.startswith(self.base):
            message = 'This Filed must start with %s!' % self.base
            raise serializers.ValidationError(message)
# 序列化器
class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={'required': '标题字段不能为空'}, validators=[XxValidator('henry')])
# 视图类
class UserGroupView(APIView):

    def post(self, request, *args, **kwargs):
        ser = UserGroupSerializer(data=request.data)
        msg = '数据提交成功'
        if ser.is_valid():
            print(ser.validated_data['title'])
        else:
            msg = ser.errors
            print(msg)
        return HttpResponse('%s' % msg)
```

#### 2. 使用钩子函数

```python

```



## 7. 分页**

### 1. 三类分页

-   看第n页，每页显示n条数据
-   在第n个位置，向后查看n条数据
-   加密分页，只能看上一页和下一页

### 2. 第一种分页

#### 1. 使用PageNumberPagination

-   utils目录下的，serializers.py

```python
# 序列化器
from rest_framework import serializers
from app01 import models

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'
```

-   直接使用PageNumberPagination，默认不可以调整每页显示的个数，配置文件固定

```python
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class Page1View(APIView):
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()
		# 实例化 PageNumberPagination 类
        pg = PageNumberPagination()
        # 获取分页对象
        page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        print(page_roles)
        # 对分页数据仅进行序列化
        ser = PageSerializer(instance=page_roles, many=True)
        return Response(ser.data)
```

-   settings.py

```python
REST_FRAMEWORK = {
    ...,
    'PAGE_SIZE': 3,
}
```

-   urls.py

```python
urlpatterns = [
   	...
    # 分页
    url(r'^(?P<version>[v1|v2]+)/page1/$', views.Page1View.as_view()),
]
```

#### 2. 自定义分页器

```python
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):
    # 每页显示个数
    page_size = 2
    # 通过page指定哪一页
    page_query_param = 'page'
    # 指定每页显示条数
    page_size_query_param = 'size'
    # 指定每页最大的数据量
    max_page_size = 5

class Page1View(APIView):
    def get(self, request, *args, **kwargs):
        ...
        pg = MyPagination()
		...
        # 带有上一页和下一页的链接
    	return pg.get_paginated_response(ser.data)
```

### 2. 第二种分页

#### 1. 使用LimitOffsetPagination

-   使用原生的分页器

```python
from rest_framework.pagination import LimitOffsetPagination

class Page1View(APIView):
    def get(self, request, *args, **kwargs):
        ...
        pg = LimitOffsetPagination()
        ...
```

#### 2. 自定义分页

````python
class MyPagination(LimitOffsetPagination):
    # 默认一页显示数据量
    default_limit = 2
    # 指定一页显示数据量
    limit_query_param = 'limit'
    # 指定数据开始位置 + 1
    offset_query_param = 'offset'
    # 限定每页最多显示的数据
    max_limit = 6

class Page1View(APIView):
    def get(self, request, *args, **kwargs):
        ...
        pg = MyPagination()
       	...
````

### 3. 第三种分页

#### 1. 自定义分页器

```python
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination

class MyPagination(CursorPagination):

    cursor_query_param = 'cursor'
    page_size = 2 
    # 排序规则
    ordering = 'id'
    page_size_query_param = 'size'
    max_page_size = 6

class Page1View(APIView):
    def get(self, request, *args, **kwargs):
        ...
        pg = MyPagination()
       	...
```

### 4. 总结

1.  数据量大，如何分页？
    -   使用`rest_framework`中的分页器，显示上一页和下一页
    -   数据库性能，可以向restful中引出
2.  flask中使用 `flask_restful`组件

```python
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class UserAPI(Resource):
    def get(self, uid):
        return {'User': 'GET'}

    def put(self, uid):
        return {'User': 'PUT'}

    def delete(self, uid):
        return {'User': 'DELETE'}

    # 添加认证
    decorators = [auth.login_required]

if __name__ == '__main__':
    app.run()
```

-   绑定路由

```python
api.add_resource(UserAPI, '/users/<int:uid>', '/u/<int:uid>')
```

## 8. 视图**

### 1. GenericAPIView

-   `class GenericAPIView(views.APIView):pass`

```python
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

class View1View(GenericAPIView):
    queryset = models.Role.objects.all()
    serializer_class = PageSerializer
    pagination_class = PageNumberPagination

    def get(self, reqeust, *args, **kwargs):
        # 获取数据
        roles = self.get_queryset()
        # 获取分页的数据
        page_roles = self.paginate_queryset(roles)
        # 序列化
        ser = self.get_serializer(instance=page_roles, many=True)
        return Response(ser.data)
```

### 2. GenericViewSet

-   可以把获取多条数据和单条数据，通过 url 中的关系进行区分
-   `class GenericViewSet(ViewSetMixin, generics.GenericAPIView):pass`
-   只是增加了方法名的映射，其他功能和`GenericAPIView`完全一样

```python
from rest_framework.viewsets import GenericViewSet

class View2View(GenericViewSet):
	...    
    def list(self, reqeust, *args, **kwargs):
        ...
        return Response(ser.data)
  
    def create(self, reqeust, *args, **kwargs):
        pass
```

#### 2. url.py

```python
urlpatterns = [
    # 视图
	url(r'^(?P<version>[v1|v2]+)/view/$', views.ViewView.as_view({'get': 'list', 'post':'create'})),
]
```

### 3. mixins系列

-   ListModelMixin：实现 `list`方法
-   CreateModelMixin：实现 `create`方法

```python
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin

class ViewView(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PageSerializer
    pagination_class = PageNumberPagination
```

### 4. ModelViewSet

-   modelviewset继承的类

````python
class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    pass
````
- 直接继承**ModelViewSet**
```python
from rest_framework.viewsets import ModelViewSet

class ViewView(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PageSerializer
    pagination_class = PageNumberPagination
```

-   urls.py

```python
urlpatterns = [
    ...
	url(r'^(?P<version>[v1|v2]+)/view/$', views.ViewView.as_view({'get':'list',  'post':'create'})),
    url(r'^(?P<version>[v1|v2]+)/view/(?P<pk>\d+)$',
        views.ViewView.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch':'partial_update'})),
]
```

![restful的view](/Users/henry/Documents/截图/Py截图/restful的view.png)

## 9. 路由**

### 1. 路由配置

-   通过路由，区分不同格式的请求URL，响应不同格式的数据

```python
urlpatterns = [
    ...
    url(r'^(?P<version>[v1|v2]+)/view/$', views.ViewView.as_view({'get': 'list', 'post': 'create'})),
    url(r'^(?P<version>[v1|v2]+)/view/(?P<format>\w+)/$', views.ViewView.as_view({'get': 'list', 'post': 'create'})),
    url(r'^(?P<version>[v1|v2]+)/view/(?P<pk>\d+)/$', views.ViewView.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'})),
    url(r'^(?P<version>[v1|v2]+)/view/(?P<pk>\d+)/(?P<format>\w+)/$', views.ViewView.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'})),
]
```

### 2. 自动生成路由

```python
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'xxx', views.ViewView)
router.register(r'yyy', views.ViewView)
urlpatterns = [
    ...
	url(r'^(?P<version>[v1|v2]+)/', include(router.urls)),
]
```

## 10. 渲染器*

### 1. 注册app

-   settings.py

```python
INSTALLED_APPS = [
  	...,
    'rest_framework',
]
```

-   views.py

```python
"""带渲染器"""
from rest_framework.response import Response
class Page1View(APIView):

    def get(self, request, *args, **kwargs):
        roles = models.Role.objects.all()
        ser = PageSerializer(instance=roles, many=True)
        print(ser.data)
        return Response(ser.data)
```

### 2. 使用

-   使用时，只要写`renderer_classes = [JSONRenderer, BrowsableAPIRenderer]`即可

```python
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer

class TestView(APIView):
	# 写入配置文件
	# renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request, *args, **kwargs):
        roles = models.Role.objects.all()
        pg = PageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        print(page_roles)
        ser = PageSerializer(instance=page_roles, many=True)
        return Response(ser.data)
```

-   配置文件

```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer', 
        'rest_framework.renderers.BrowsableAPIRenderer'
    ],
}
```

## 11. contenttype组件

### 1. 作用

-   django内置的一个组件，帮助开发者做连表操作
-   一张表和多张表中的数据同时关联时，需要使用

### 2. 使用

#### 1. models.py

-   GenericForeignKey
-   GenericRelation

```python
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
# 普通课程表
class Course(models.Model):
    """普通课程"""
    title = models.CharField(max_length=32)
    # 仅用于反向查找，不会在数据库中生成
    price_policy_list = GenericRelation('PricePolicy')
# 学位课程表
class DegreeCourse(models.Model):
    """学位课程"""
    title = models.CharField(max_length=32)
    price_policy_list = GenericRelation('PricePolicy')
# 价格策略表
class PricePolicy(models.Model):
    price = models.IntegerField()
    period = models.IntegerField()
    # 具体 app 和 model 名称
    content_type = models.ForeignKey(ContentType, verbose_name='关联表名称')
    object_id = models.IntegerField(verbose_name='关联表数据ID')
    # 快速实现 content_type 操作
    content_obj = GenericForeignKey('content_type', 'object_id')
```

#### 2. views.py

```python
from django.http import HttpResponse
from app01 import models

def test(request):
    # 添加数据
    obj = models.DegreeCourse.objects.filter(title='python全栈').first()
    models.PricePolicy.objects.create(price=9.9, period=30, content_obj=obj)

    obj = models.DegreeCourse.objects.filter(title='python全栈').first()
    models.PricePolicy.objects.create(price=19.9, period=60, content_obj=obj)

    obj = models.DegreeCourse.objects.filter(title='python全栈').first()
    models.PricePolicy.objects.create(price=29.9, period=90, content_obj=obj)

    return HttpResponse('ok')

```

#### 3. 根据课程id获取课程

-   `GenericRelation('PricePolicy')`
-   查找数据库时，使用

```python
course = models.Course.objects.filter(id=1).first()
# 获取所有课程对象 
price_poicy = course.price_policy_list.all()
```
