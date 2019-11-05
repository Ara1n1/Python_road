# 1. 项目创建流程

1. 创建虚拟环境(使用pycharm下载)

   - 新建django项目师，创建虚拟环境，pycharm默认会安装最新版的django
   - 在普通的django中创建虚拟环境，之后使用虚拟环境创建Django
   - **勾选** make  avaliable to all projects

2. 下载Django包

   - 创建django项目，如果没有虚拟项目需要手动添加虚拟环境的解释器

3. 创建django项目和app1(**web**)

   - 主要用于web页面的展示和处理

4. 测试用的数据库不同

   - 新建**local_settings**.py 文件

   ```python
   # local_settings.py
   import os
   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   ALLOWED_HOSTS = []
   # 用于本地debug
   DEBUG = True
   DATABASES = {
   	'default': {
   		'ENGINE': 'django.db.backends.sqlite3',
   		'NAME': os.path.join(BASE_DIR, 'db.local_sqlite3'),}
   }
   ```

   - **settings**.py文件需要导入本地测试配置文件

   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['*']
   LANGUAGE_CODE = 'zh-hans'
   TIME_ZONE = 'Asia/Shanghai'
   USE_L10N = False
   DATE_FORMAT = 'Y/m/d'
   DATETIME_FORMAT = 'Y/m/d H:i:s'
   
   STATICFILES_DIRS = [
       os.path.join(BASE_DIR, 'static')
   ]
   # 需要导入local_settings.py中的所有变量
   # 线上使用没有local_settings.py 文件，需要进行异常处理
   try:
   	from .local_settings import *
   except ImportError:
     pass
   ```

5. git版本控制(.gitignore)

   - 忽略虚拟环境目录
   - github找忽略文件，添加.idea/、db.local_sqlite3

6. 创建**app2**：backend

   - 用于后台管理

7. 创建**app3**：repository

   - 用于models的创建

# 2. 上传文件

1. 富文本编辑框

2. 伪静态地址**xx/x.html**（seo）

3. pycharm查找可以使用命名分组进行查找和替换

4. 设计表结构

   - 类别表
     1. 列表的名称
     2. 文章详情表

   - content(textfield)

   - 文章表
     1. title
     2. create_at
     3. profile
     4. category(外键类别表)
     5. content(外键关联文章详情表)

## 1. meida的配置

- pycharm中使用正则进行匹配和替换

```python
../../(.*?)
{% static '$1' %}
```

### 1.1 配置settings.py

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 1.2 配置urls.py

```python
# 项目根的urls.py
from django.views.static import serve
from django.conf import settings
urlpatterns = [
  	url(r'^media/(?P<path>.*)', serve, {'document_root':settings.MEDIA_ROOT})
]
```

### 1.3 ImageField()下载pillow

```python
# 下载pillow包
pip install pillow
```

### 1.4 models.py使用

- 更改完成后使用迁移命令

```python
from django.db import models

class Article(models.Model):
		img = ImageField(upload_to='img/article/', verbose_name='图片')
```

## 2. 富文本编辑器

### 1. 需要下载

- django-ckeditor

```python
# ckeditor
pip install django-ckeditor
```

### 2. 配置文件(2)

```python
# 项目的setting.py
1. 注册 ckedior app
INSTALLED_APPS = [
  	'ckeditor',
	'ckeditor_uploader',
]
2. 配置文件上传路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CKEDITOR_UPLOAD_PATH = 'ckeditor/'
```

### 3. 在**model.py**中使用字段

- 导入和使用

```python
from ckeditor_uploader.fields import RichTextUploadingField

class ArticleDetail(models.Model):
		content = RichTextUploadingField(verbose_name='文章详情')
```

### 4. 配置url

- 配置url，注意url顺序

```python
from ckeditor_uploader import views
from django.views.static import serve
urlpatterns = [
  	url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='img'),
  	url(r'^ckeditor/upload/', views.upload),
	url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
```

### 5. 在模版中导入js

```django
<script src="{% static 'ckeditor/ckeditor/ckeditor.js' %}"></script>
<script src="{% static 'ckeditor/ckeditor-init.js' %}"></script>
```

### 6. 使用

- models文件使用富文本之后
- 迁移数据库

```python
# repository中的 models.py
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
  	name = models.CharField('分类名', max_length=16)
    
class ArticleDetail(models.Model):
		content = RichTextUploadingField(verbose_name='文章详情')

class Article(models.Model):
  	title = models.CharField('文章标题', max_length=32)
    profile = models.CharField('文章简介', max_length=256)
    img = models.ImageField(upload_to='img/article/', verbose_name = '显示图片')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    category = models.ForeignKey('Category', blank=True, null=True, verbose_name='文章类别')
    # OneToOneField：一对一，并且外键唯一，包含 unique 约束
    detail = models.OneToOneField('ArticleDetail', verbose_name='文章详情')
```

# 3. 滚动请求数据

## 1. url设计

```python
url(r'^(learning_notes|student_evaluation|student-interview).html', views.feedback_list, name='feedback')
```

## 2. 静态页面

- web中的template
- 继续使用模板和继承

## 3. pycharm

```python
# pycharm比较文件或文件夹的不同
compare with
```

## 4. 使用字典取值传参

- 使用字典进行banner和title的分类

- 使用模版进行渲染

## 5. models设计

- 数据库迁移

```python
# repository中的models.py
from django.db import models
class Feedback(models.Model):
  	type_choice = ((0, '未分类'), (1,'学习笔记'), (2, '学员评价'), (3, '入职邀约'),)
  	img = models.ImageField(upload_to='img/feedback/')
    img_type = models.IntegerField(choices=type_choice, default=0)
```

## 2. 滚动尾页请求数据

### 1. 设计url

```python
# urls.py
urlpatterns = [
  	url(r'^ajax_feedback/', views.AjaxFeedback.as_view()),
]
```

### 2. 请求分页使用流程

#### 1. 下载和注册

- djangorestframework

```python
# 一般使用pycharm安装
pip install djangorestframework
```

- 注册

```python
# 注册app
'rest_framwork'
```

#### 2. 使用modelserializer

- **类变量(5)**：queryset、serializer_class、pagination_class、filter_backends和filter_fields

```python
# views.py
from repository import models
from rest_framework import generics
from web.serializer import FeedbackSerializer
from web.pagination import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend

class AjaxFeedback(generics.ListAPIView):
    queryset = models.Feedback.objects.all()
    # 序列化器
    serializer_class = FeedbackSerializer
    # 分页器
    pagination_class = DefaultPagination
    # 过滤条件，和过滤依据
    filter_backends = [DjangoFilterBackend, ]
    filter_fields = ['img_type']
```

#### 3. 序列化器

- **除了继承类，与modelform写法完全相同**

```python
# serializer里的__init__.py中
from rest_framework import serializers
from repository import models

class FeedbackSerializer(serializers.ModelSerializer):
  	class Meta:
      	model = models.Feedback
        fields = ['img']
```

#### 4. 分页器

- **类变量(4)**：page_size、page_query_param、(page_size_query_param、max_page_size)

```python
# pagination里的__init__.py中
from rest_framwork.pagination import PageNumberPagination
class DefaultPagination(PageNumberPagination):
  	# 一页的数据
  	page_size = 8
    # 分页查询条件的key
    page_query_param = 'page'
    # 当定义page_size有效
    page_size_query_param = 'size'
    max_page_size = 4
```

### 3. 筛选条件使用流程

#### 1. 下载django-filter

```python
# 一般使用pycharm
pip install django-filter
```

#### 2. 注册app

```python
'django_filters'
```

#### 3. models中使用

```python
from django_filters.rest_framework import DjangoFilterBackend

class AjaxFeedback(serializers.ModelSerializer):
		# 过滤条件，和过滤依据
    filter_backends = [DjangoFilterBackend, ]
    filter_fields = ['img_type']
```

## 3. 滚动触发ajax

- ajax属于异步请求，需要使用**tag**标志，转换成同步
- 这里的data返回的是一个js对象(相当于python的字典)

```js
$(function () {
    var img_type = $('.thisli').attr('img_type');
    var page = 1;		// 请求的页码
    var num = 0;		// 当前请求数据的总条数
    var next = 1;		// data中的字段 next是下次请求的url
    var tag = 1;		// 用于标示当前是否有ajax请求

    function get_info() {

        if (next && tag) {
            tag = 0;
            $.ajax({
                url: `/ajax_feedback/?img_type=${img_type}&page=${page}`,
                success: function (data) {
                    // console.log(data);
                    var results = data.results;
                    next = data.next;

                    for (var i in  results) {
                        var row = results[i];
                        var col = $('.column')[num % 4];
                      	// 需要加入的 html 标签
                        var item = `<div class="item">
                                    <div class="animate-box">
                                    <a href="${row.img}"class="image-popup fh5co-board-img">
                                     <img src="${row.img}"alt="Free HTML5 Bootstrap template">
                                    </a>
                                    </div>
                                    </div>`;
                      
                        $(col).append(item);
                        magnifPopup();
                        animateBoxWayPoint();
                        num += 1
                    }

                    page += 1;
                    tag = 1;
                }
            })
        }
    }

    get_info();
    //同学说分批加载
    $(window).scroll(function () {
        //$(document).scrollTop() 滚动条位置距页面顶部的距离；
        //$(document).height() 整个页面的总高度；
        //$(window).height() 当前窗口的高度；
        //判断是否已经滚动到页面底部；
        if ($(document).scrollTop() >= $(document).height() - $(window).height() - 180) {
            get_info();
        }
    });
}());
```

# 4. RESTful

## 1. REST

Respresentation State Transfer

## 2. RESTful API设计

1. api与用户的通信协议，推荐使用https
2. 域名
   1. `https://api.example.com `尽量将api部署在专用域名(会存在跨域问题)
   2. `https://example.org/api/ `api很简单
3. 版本
   - url 如：`https://api.example.com/v1/`
   - 版本加在请求头中
4. 路径，网络上任何东西都是资源，**均使用名词表示**(可复数)
5. method
   1. GET 获取服务器上的资源，返回**资源列表或一个资源**
   2. POST 新建资源，**返回新建资源**
   3. PUT 在服务器更新资源(客户端提供改变后的完整资源)，**返回更改后的资源**
   4. PATCH 在服务器更新资源(更改某些数据)
   5. DELETE 删除资源，**返回空/提示**
   6. **出错返回信息**
6. 过滤，通过url上传参形式
   1. `https://api.example.com/v1/zoos?limit=10`
   2. `https://api.example.com/v1/zoos?offset=10`
   3. ...
7. 状态码
   1. 200 ok
   2. 201 created  **[POST/PUT/PATCH]**：用户新建或修改数据成功
   3. 201 Accepted 表示需要排队，异步
   4. 204 No content **[DELETE]**：用户删除数据成功
   5. 错误处理，状态码4xx，应返回错误信息，error当作key
      - 401验证失败，403权限不足，404资源不存在
8. Hypermedia API **返回关联的数据时，尽量返回url地址**

`www.ruanyifeng.com/blog/2014/05/restful_api.html`

## 3. 使用rest_framwork流程

- **JsonResponse可以序列化datetime类型**
  1. `[{"id": 1, "title": "python之旅", "pub__name": "工业出版社", "authors": 1},{"id": 1, "title": "python之旅", "pub__name": "工业出版社", "authors": 2}...]`
  2. **数据有冗余，无法展示出版社名称和作者名称**

```python
from django.http.response import JsonResponse
class BookListView(APIView):

	def get(self, request, *args, **kwargs):
		all_book = models.Book.objects.all().values('id', 'title', 'pub__name', 'pub_date', 'authors')
		return JsonResponse(data=list(all_book), json_dumps_params={'ensure_ascii': False}, safe=False)
```

- **django提供的序列化器**
  1. [{"model": "app01.book", "pk": 1, "fields": {"title": "python之旅", "price": "59.99", "pub": 2, "authors": [1, 2]}},
  2. **层级深，无法展示出版社名称和作者名称**

```python
"""数据的序列化器"""
from django.http.response import HttpResponse
from django.core import serializers

class BookListView(APIView):
	def get(self, request, *args, **kwargs):
		all_book = models.Book.objects.all()
		ser_obj = serializers.serialize('json', all_book, ensure_ascii=False)
		return HttpResponse(ser_obj)
```

### 1. 注册rest_framework app 

1. **不使用序列化器时**，多对多关系对应多个值时，**会分别为关联值构造不同的字典**
2. `[{"id":1,"title":"python之旅","price":"59.99","pub":{"name":"工业出版社"},"authors":[{"name":"echo"},{"name":"henry"}]}`
3. **外键是字典，多对多是列表套字典**
4. rest_framework的**Response()不能序列化对象**

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class BookListView(APIView):
  	def get(self, request, *args, **kwargs):
      	all_book = models.Book.object.all().values('id', 'title', 'auther__name')
        return Response(all_book)
```

### 2. 使用序列化器精简数据

- 多对多关系使用**authors = serializers.SerializerMethodField(read_only=True)**方法
- 需要实现**get_authors**方法

#### 2.1 写法一(Serializer)

- 类似form与modelform 的关系，写法几乎相同

```python
# serializer.py文件，app目录下
from rest_framework import serializers
from app01 import models

class Publisherserializer(serializers.Serializer):
  	name = serializers.CharField()

class AuthorSerializer(serializers.Serializer):
  	id = serializers.IntegeField()
  	name = serializers.CharField()
   
class BookSerializer(serializers.Serializer):
  	title = serializers.CharField()
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    pub_date = serializers.DateTimeField()
    # 外键
    # pub_id = serializers.IntegeField()
    pub = Publisherserializer(required=False, read_only=True)
    # 多对多，需要实现get_authors 方法
    authors = serializers.SerializerMethodField(read_only=True)
    
    # post请求
    post_pub = serializers.CharField(write_only=True)
    post_authors = serializers.ListField(write_only=True)
    
    def get_authors(self, obj):
      	ser_obj = AuthorSerializer(obj.authors.all(), many=True)
      	return ser_obj.data
    # post操作调用
    def create(self, validated_data):
      	book = models.Book.objects.create(
            title=validated_data['title'],
            price=validated_data['price'],
            pub_date=validated_data['pub_date'],
            pub_id=validated_data['post_pub'],
        	)
        book.authors.set(validated_data['post_author'],)
        return book
    # put操作调用
    def update(self, instance, validated_data):
      	instance.title=validated_data.get('title', instance.title)
        instance.price=validated_dataget('price', instance.price)
        instance.pub_date=validated_dataget('pub_date', instance.pub_date)
        instance.pub_id=validated_dataget('pub_id', instance.pub_id)
        instance.save()
        instance.authors.set(validated_data.get('post_author', instance.authors.all()),)
        return instance   	
```

#### 2.2 写法二(ModelSerializer)

- 局部校验

```python
class BookSerializer(serializers.Serializer):
		title = serializers.CharField(max_length=32)
    ...
    def validate_title(self, value):
        if 'xx' in value:
            raise serializers.ValitdatoinError
        return value
```

- 全局校验

```python
class BookSerializer(serializers.Serializer):
		title = serializers.CharField(max_length=32)
    ...
    # attrs为有序字典，所有数据
    def validate(self, attrs):
        pass
```

- 自定义校验

```python
# 类似于Form组建中的自定义校验规则
def my_validata(value)
    if 'xx' in value:
      	raise serializers.ValitdatoinError
    return value
      
class BookSerializer(serializers.Serializer):
		title = serializers.CharField(max_length=32, validators=[my_validata, ])
		...
```

- **使用ModelSerializer**

```python
class BookSerializer(serializers.ModelSerializer):
  	pub_info = serializers.SerializersMethodField(read_only=True)
    author_info = serializers.SerializersMethodField(read_only=True)
    
    def get_pub_info(self, obj):
      	return PublisherSerializer(obj.pub).data
      
    def get_pub_info(self, obj):
        return AuthorSerializer(obj.authors.all(), many=True).data
    
  	class Meta:
      	model = models.Book
        fields = '__all__'
        # 取值深度，用来读取，即GET请求
        # depth = 1 
        extra_kwargs = {
          	'pub':{'write_only':True},
          	'authors':{'write_only':True},
         }
```

### 3. 导入view.py中使用

1. 使用序列化器时，默认情况下一次只能序列化**一个对象**，如果是对象列表则需要使用**many=True**参数
2. 使用**rest_framework**序列化器后，WSGI封装的**request**此时为 **request._request**
3. 序列化后的对象，**obj.data**即为从数据库中读取的数据，tpye为**ordereddict的list**
   - [OrderedDict([(), ()…]), OrderedDict([(), ()…]), … ]

```python
# app的views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from app01 import models
from app01.serializer import BookSerializer


class BookListView(APIView):
	book_obj = {}

    def get(self, request, pk=None, *args, **kwargs):
        if not pk:
          	all_book = models.Book.objects.all()
        else:
            all_book = models.Book.objects.filter(pk=pk)
            self.book_obj['obj'] = all_book.first()
            
        ser_obj = BookSerializer(all_book, many=True)
        # print(ser_obj.data, type(ser_obj.data))
        # .data获取序列化结果
        return Response(ser_obj.data)

    def post(self, request, *args, **kwargs):
      	# 必须使用application/x-www-form-urlencoded，表单数据
      	# print(request.POST)
        # 使用必须使用application/json, 获取的是dict类型，request发生了变化
        # print(request.data, type(request.data))
        # print(request.data)
        ser_obj = BookSerializer(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save()
            return Response(ser_obj.data)
        return Response(ser_obj.errors)

    def put(self, request, *args, **kwargs):
        obj = self.book_obj.get('obj')
        if not obj:
          	return Response('更新数据不存在')

       	ser_obj = BookSerializer(instance=obj, data=request.data, partial=True)
				if ser_obj.is_valid():
						ser_obj.save()
						return Response(ser_obj.data)
				return Response(ser_obj.errors)

    def delete(self, requset, pk, *args, **kwargs):
        obj = models.Book.objects.filter(pk=pk)
        if obj:
            obj.delete()
            return Response({'msg': '删除成功'})
         return Response({'msg': '数据不存在'})
```

# 5. 极验验证码和短信验证

- **下载python包：reqeusts、geetest、aliyun-python-sdk**

## 1. 设计login的url

- login使用CBV

```python
# 相当于初始化
url(r'^pc-geetest/register', views.pcgetcaptcha, name='pcgetcaptcha'), 
# 二次验证
url(r'^pc-geetest/ajax_validate', views.pcajax_validate, name='pcajax_validate'),  
# 登录校验
url(r'login.html', views.Login.as_view(), name='login'),
```

## 2. 使用对应的view函数

```python
# 行为验证初始化
def pcgetcaptcha(request):
	user_id = 'test'
	gt = GeetestLib(settings.PC_GEE_ID, settings.PC_GEE_KEY)
	status = gt.pre_process(user_id)
	request.session[gt.GT_STATUS_SESSION_KEY] = status
	request.session["user_id"] = user_id
	response_str = gt.get_response_str()
	return HttpResponse(response_str)
# 二次验证
def pcajax_validate(request):
    if request.method == "POST":
        gt = GeetestLib(settings.PC_GEE_ID, settings.PC_GEE_KEY)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
        		result = gt.success_validate(challenge, validate, seccode, user_id)
      	else:
        		result = gt.failback_validate(challenge, validate, seccode)
      	if result:
            result = {"status": "success"}
            # 二次校验成功
            # 发短信，并存储code
            code = sms.getcode()
            phone = request.POST.get('phone')
            sms.send_sms(phone, code)
            request.session['code'] = code
     	 	else:
        		result = {"status": "fail"}
      	return HttpResponse(json.dumps(result))
    return HttpResponse("error")
```

## 3. 修改js

1. 根据业务逻辑进行修改**js**流程
2. 添加和修改错误提醒
3. 调整二次验证的

```js
// 短信+极验行为验证
var num = 60;
$('.getcode').click(function () {
    var flag = /^1[3-9][0-9]{9}$/.test($('#phone').val());
    if (!flag) {
        $('.error-wrap').show();
        $('.sms-login .phone').addClass('error-box');
        return;
    }
 		// 判断极验图片验证是否合法
    validate = obj.getValidate();
    if (!validate) {
        $('.error-wrap').show();
        $('.error-wrap span').text('请先点击按钮进行验证');
        $('.sms-login .validate').addClass('error-box');
        return;
    }
		// 二次验证，并进行短信发送，flag用于区分登录方式
    $.ajax({
        url: "/pc-geetest/ajax_validate", // 进行二次验证
        type: "post",
        dataType: "json",
        data: {
            flag:'sms',
            phone: $('#phone').val(),
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']" ).val(),
            geetest_challenge: validate.geetest_challenge,
            geetest_validate: validate.geetest_validate,
            geetest_seccode: validate.geetest_seccode
          }
    });
  // 获取验证码倒计时
    var _this = $(this);
    $('.countdown').find('span').text(num);
    var timer = setInterval(function () {
      	if (num > 0) {
            $('.countdown').find('span').text(num--);
            _this.hide();
            $('.countdown').show();
      	} else {
            clearInterval(timer);
            num = 60;
            _this.show();
            $('.countdown').hide();
      }
    }, 1000)
  	});

		var obj = null;
		//滑动验证码 geetest网站:https://docs.geetest.com/install/deploy/server/python
    var handlerEmbed = function (captchaObj) {
      	obj = captchaObj;
        $("#embed-submit").click(function (e) {
            var validate = captchaObj.getValidate();
            if (!validate) {
                $("#notice")[0].className = "show";
                setTimeout(function () {
                  	$("#notice")[0].className = "hide";
                }, 2000);
                e.preventDefault();
            }
      });
      // 将验证码加到id为captcha的元素里，同时会有三个input的值：geetest_challenge, geetest_validate, geetest_seccode
      captchaObj.appendTo("#embed-captcha");
      captchaObj.onReady(function () {
        $("#wait")[0].className = "hide";
      });
    };
    $.ajax({
        // 获取id，challenge，success（是否启用failback）
        url: "/pc-geetest/register?t=" + (new Date()).getTime(), // 加随机数防止缓存
        type: "get",
        dataType: "json",
        success: function (data) {
            // 使用initGeetest接口
            // 参数1：配置参数
            // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
            initGeetest({
              gt: data.gt,
              challenge: data.challenge,
              product: "float", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
              offline: !data.success, // 表示用户后台检测极验服务器是否宕机，一般不需要关注
              new_captcha: data.new_captcha,
              api_server: "api.geetest.com"
          }, handlerEmbed);
      }
    });
```

- **js中的正则表达式**

```js
phone_num = $('#phone').val()
flag = /^1(3-9)[0-19]{9}$/.test(phone)
if (!flag){
  	return
}
...
```

- **极验验证流程**

![geetest_justify](/System/Volumes/Data/Users/henry/Documents/截图/Py截图/geetest_justify.jpg)

## 4. 配置文件

```python
# 验证码的id和key，需要注册
PC_GEE_ID = '13e4f7b3b8323da2b0ff9950b7ab76bc'
PC_GEE_KEY = '2b7352c63ed6252df1762fb29c54ee92'
# 短信验证码
ACCESSKEY_ID = "LTAIOj7VnM7ho77j"
ACCESS_KEY_SECRET = 'pKGn0wNVezkcjzhKwR1xi69XgCJQ22'

SMS_TEMPLATE_CONF = {'TemplateCode': 'SMS_167972102',
					 'TemplateParam': '{"code":"%s"}',
					 'SignName': "14K"}
```









