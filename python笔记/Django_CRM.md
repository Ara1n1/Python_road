# 1. 登陆和注册

## 1.1 forms

- 自动生成前端标签

```python
# crm中的forms.py
import hashlib
from django import forms
from django.core.exceptions import ValidationError
from crm import models

class RegForm(forms.ModelForm):
  	# 由于类中没有re_password,需要进行手写（优先级高于自动生成）
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': "您的密码", 'autocomplete': "off", }))
    re_password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': "确认您的密码", 'autocomplete': "off", }))
    class Meta:
        model = models.UserProfile
        # __all__表示生成类中的所有字段, fields也支持[字段名1，字段名2...]
        fields = '__all__'
        # 表示排除某些字段
        exclude = ['is_active',]
        # 多个字段写在一起的插件
        widgets = {
            'username': forms.EmailInput(attrs={'placeholder': "您的用户名", 'autocomplete': "off", }),
            'name': forms.TextInput(attrs={'placeholder': "您的名字", 'autocomplete': "off", }),
            'mobile': forms.TextInput(attrs={'placeholder': "您的手机号", 'autocomplete': "off", }),}
        # 自定义错误信息
        error_messages = {
            'username': {
                'required': '信息不能为空',
                'invalid': '邮箱格式不正确',}}
    def clean(self):
      	self._validate_unique=True / super().clean()
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        print(self.cleaned_data.get('department'))
        if password == re_password:
            md = hashlib.md5(b'sajdfkh')
            md.update(password.encode('utf-8'))
            self.cleaned_data['password'] = md.hexdigest()
            return self.cleaned_data
        
        # 把错误信息加载到，某个字段的错误中
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次密码不一致')
```

## 1.2 html页面

### 1. 注册页面

```html
<!DOCTYPE html>
<html lang="en">
<head>
    {% load static %}
    <meta charset="UTF-8">
    <title>注册</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>

<div class="register-container">
    <h1>Welcom to sign up Henry's CRM</h1>
    <div class="connect">
        <p>Link the world. Share to world.</p>
    </div>
    <form action="" method="post" id="registerForm" novalidate="novalidate">
        {% csrf_token %}
        <div>
            {{ form_obj.username }}
            {{ form_obj.username.errors.0 }}
        </div>
        <div>
            {{ form_obj.password }}
            {{ form_obj.password.errors.0 }}
        </div>
        <div>
            {{ form_obj.re_password }}
            {{ form_obj.re_password.errors.0 }}
        </div>
        <div>
            {{ form_obj.name }}
            {{ form_obj.name.errors.0 }}
        </div>
        <div>
            {{ form_obj.mobile }}
            {{ form_obj.mobile.errors.0 }}
        </div>
        <div>
            {{ form_obj.department}}
            {{ form_obj.department.errors.0 }}
        </div>
        <button id="submit" type="submit">注 册</button>
    </form>
    <a href="/crm/login">
        <button type="button" class="register-tis">已经有账号？</button>
    </a>
</div>

<script src="{% static 'js/jquery.min.js' %}"></script>
<script src="{% static 'js/common.js' %}"></script>
<script src="{% static 'js/supersized.3.2.7.min.js' %}"></script>
<script src="{% static 'js/supersized-init.js' %}"></script>
<script src="{% static 'js/jquery.validate.min.js' %}"></script>
</body>
</html>
```

### 2. 登陆页面

```html
<!DOCTYPE html>
<html lang="en">
<head>
    {% load static %}
    <meta charset="UTF-8">
    <title>登陆</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>

<div class="login-container">
    <h1>Henry's CRM</h1>
    <div class="connect">
        <p>Link the world. Share to world.</p>
    </div>
    <form action="" method="post" id="loginForm" novalidate="novalidate">
        {% csrf_token %}
        <div>
            <input type="text" name="username" class="username" placeholder="用户名" autocomplete="off">
        </div>
        <div>
            <input type="password" name="password" class="password" placeholder="密码" oncontextmenu="return false"
                   onpaste="return false">
        </div>
        <div>
            {{ error }}
        </div>
        <button id="submit" type="submit">登 陆</button>
    </form>
    <a href="/crm/reg/">
        <button type="button" class="register-tis">还有没有账号？</button>
    </a>
</div>

<script src="{% static 'js/jquery.min.js' %}"></script>
<script src="{% static 'js/common.js' %}"></script>
<script src="{% static 'js/supersized.3.2.7.min.js' %}"></script>
<script src="{% static 'js/supersized-init.js' %}"></script>
<script src="{% static 'js/jquery.validate.min.js' %}"></script>
</body>
</html>
```

## 1.3 业务逻辑

```python
import hashlib
from django import forms
from django.core.exceptions import ValidationError
from crm import models

class RegForm(forms.ModelForm):
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': "您的密码", 'autocomplete': "off", }))
    re_password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': "确认您的密码", 'autocomplete': "off", }))

    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = ['is_active']
        widgets = {
            'username': forms.EmailInput(attrs={'placeholder': "您的用户名", 'autocomplete': "off", }),
            'name': forms.TextInput(attrs={'placeholder': "您的名字", 'autocomplete': "off", }),
            'mobile': forms.TextInput(attrs={'placeholder': "您的手机号", 'autocomplete': "off", }),}
        error_messages = {
            'username': {
                'required': '信息不能为空',
                'invalid': '邮箱格式不正确',}}

    def clean(self):
        # self._validate_unique = True
        super().clean()    # 校验邮箱名是否已经在数据库中
        password = self.cleaned_data.get('password', '')
        re_password = self.cleaned_data.get('re_password')
        if password == re_password:
            md = hashlib.md5(b'sajdfkh')
            md.update(password.encode('utf-8'))
            self.cleaned_data['password'] = md.hexdigest()
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次密码不一致')
```

### 1.4 models.py

- 数据表的创建

```python
from django.db import models
from multiselectfield import MultiSelectField

course_choices = (('Linux', 'Linux中高级'),
                  ('PythonFullStack', 'Python高级全栈开发'),)

class_type_choices = (('fulltime', '脱产班',),
                      ('online', '网络班'),
                      ('weekend', '周末班',),)

source_type = (('qq', "qq群"),
               ('referral', "内部转介绍"),
               ('website', "官方网站"),
               ('baidu_ads', "百度推广"),
               ('office_direct', "直接上门"),
               ('WoM', "口碑"),
               ('public_class', "公开课"),
               ('website_luffy', "路飞官网"),
               ('others', "其它"),)

enroll_status_choices = (('signed', "已报名"),
                         ('unregistered', "未报名"),
                         ('studying', '学习中'),
                         ('paid_in_full', "学费已交齐"))

seek_status_choices = (('A', '近期无报名计划'), ('B', '1个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'),
                       ('E', '定金'), ('F', '到班'), ('G', '全款'), ('H', '无效'),)
pay_type_choices = (('deposit', "订金/报名费"),
                    ('tuition', "学费"),
                    ('transfer', "转班"),
                    ('dropout', "退学"),
                    ('refund', "退款"),)

attendance_choices = (('checked', "已签到"),
                      ('vacate', "请假"),
                      ('late', "迟到"),
                      ('absence', "缺勤"),
                      ('leave_early', "早退"),)

score_choices = ((100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (70, 'B-'), (60, 'C+'), (50, 'C'),(40, 'C-'), (0, ' D'), (-1, 'N/A'), (-100, 'COPY'), (-1000, 'FAIL'),)


class Department(models.Model):
    """
    部门表
    """
    name = models.CharField(max_length=32, verbose_name="部门名称")
    count = models.IntegerField(verbose_name="人数", default=0)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    用户表
    """
    username = models.EmailField(max_length=255, unique=True, )
    password = models.CharField(max_length=128)
    name = models.CharField('名字', max_length=32)
    department = models.ForeignKey('Department', default=None, blank=True, null=True)
    mobile = models.CharField('手机', max_length=32, default=None, blank=True, null=True)
    memo = models.TextField('备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    """
    客户表
    """
    qq = models.CharField('QQ', max_length=64, unique=True, help_text='QQ号必须唯一')
    qq_name = models.CharField('QQ昵称', max_length=64, blank=True, null=True)
    name = models.CharField('姓名', max_length=32, blank=True, null=True, help_text='学员报名后，请改为真实姓名')
    sex_type = (('male', '男'), ('female', '女'))
    sex = models.CharField("性别", choices=sex_type, max_length=16, default='male', blank=True, null=True)
    birthday = models.DateField('出生日期', default=None, help_text="格式yyyy-mm-dd", blank=True, null=True)
    phone = models.BigIntegerField('手机号', blank=True, null=True)
    source = models.CharField('客户来源', max_length=64, choices=source_type, default='qq')
    introduce_from = models.ForeignKey('self', verbose_name="转介绍自学员", blank=True, null=True)
    course = MultiSelectField("咨询课程", choices=course_choices)
    class_type = models.CharField("班级类型", max_length=64, choices=class_type_choices, default='fulltime')
    customer_note = models.TextField("客户备注", blank=True, null=True, )
    status = models.CharField("状态", choices=enroll_status_choices, max_length=64, default="unregistered",  help_text="选择客户此时的状态")
    last_consult_date = models.DateField("最后跟进日期", auto_now_add=True)
    next_date = models.DateField("预计再次跟进时间", blank=True, null=True)
    consultant = models.ForeignKey('UserProfile', verbose_name="销售", related_name='customers', blank=True, null=True, )
    class_list = models.ManyToManyField('ClassList', verbose_name="已报班级", )

    def __str__(self):
        if self.name:
            return self.name
        return 'None'


class Campus(models.Model):
    """
    校区表
    """
    name = models.CharField(verbose_name='校区', max_length=64)
    address = models.CharField(verbose_name='详细地址', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name


class ClassList(models.Model):
    """
    班级表
    """
    course = models.CharField("课程名称", max_length=64, choices=course_choices)
    semester = models.IntegerField("学期")
    campuses = models.ForeignKey('Campus', verbose_name="校区")
    price = models.IntegerField("学费", default=10000)
    memo = models.CharField('说明', blank=True, null=True, max_length=100)
    start_date = models.DateField("开班日期")
    graduate_date = models.DateField("结业日期", blank=True, null=True)
    teachers = models.ManyToManyField('UserProfile', verbose_name="老师")
    class_type = models.CharField(choices=class_type_choices, max_length=64, verbose_name='班额及类型', blank=True, null=True)

    class Meta:
        unique_together = ("course", "semester", 'campuses')

    def __str__(self):
        return '{}-{}'.format(self.get_course_display(), self.semester)


class ConsultRecord(models.Model):
    """
    跟进记录表
    """
    customer = models.ForeignKey('Customer', verbose_name="所咨询客户")
    note = models.TextField(verbose_name="跟进内容...")
    status = models.CharField("跟进状态", max_length=8, choices=seek_status_choices, help_text="选择客户此时的状态")
    consultant = models.ForeignKey("UserProfile", verbose_name="跟进人", related_name='records')
    date = models.DateTimeField("跟进日期", auto_now_add=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)


class Enrollment(models.Model):
    """
    报名表
    """

    why_us = models.TextField("为什么报名", max_length=1024, default=None, blank=True, null=True)
    your_expectation = models.TextField("学完想达到的具体期望", max_length=1024, blank=True, null=True)
    contract_agreed = models.BooleanField("我已认真阅读完培训协议并同意全部协议内容", default=False)
    contract_approved = models.BooleanField("审批通过", help_text="在审阅完学员的资料无误后勾选此项,合同即生效", default=False)
    enrolled_date = models.DateTimeField(auto_now_add=True, verbose_name="报名日期")
    memo = models.TextField('备注', blank=True, null=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)
    customer = models.ForeignKey('Customer', verbose_name='客户名称')
    school = models.ForeignKey('Campus')
    enrolment_class = models.ForeignKey("ClassList", verbose_name="所报班级")

    class Meta:
        unique_together = ('enrolment_class', 'customer')


class PaymentRecord(models.Model):
    """
    缴费记录表
    """
    pay_type = models.CharField("费用类型", choices=pay_type_choices, max_length=64, default="deposit")
    paid_fee = models.IntegerField("费用数额", default=0)
    note = models.TextField("备注", blank=True, null=True)
    date = models.DateTimeField("交款日期", auto_now_add=True)
    course = models.CharField("课程名", choices=course_choices, max_length=64, blank=True, null=True, default='N/A')
    class_type = models.CharField("班级类型", choices=class_type_choices, max_length=64, blank=True, null=True, default='N/A')
    enrolment_class = models.ForeignKey('ClassList', verbose_name='所报班级', blank=True, null=True)
    customer = models.ForeignKey('Customer', verbose_name="客户")
    consultant = models.ForeignKey('UserProfile', verbose_name="销售")
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)

    status_choices = (
        (1, '未审核'),
        (2, '已审核'),
    )
    status = models.IntegerField(verbose_name='审核', default=1, choices=status_choices)
    confirm_date = models.DateTimeField(verbose_name="确认日期", null=True, blank=True)
    confirm_user = models.ForeignKey(verbose_name="确认人", to='UserProfile', related_name='confirms', null=True, blank=True)


class CourseRecord(models.Model):
    """课程记录表"""
    day_num = models.IntegerField("节次", help_text="此处填写第几节课或第几天课程...,必须为数字")
    date = models.DateField(auto_now_add=True, verbose_name="上课日期")
    course_title = models.CharField('本节课程标题', max_length=64, blank=True, null=True)
    course_memo = models.TextField('本节课程内容', max_length=300, blank=True, null=True)
    has_homework = models.BooleanField(default=True, verbose_name="本节有作业")
    homework_title = models.CharField('本节作业标题', max_length=64, blank=True, null=True)
    homework_memo = models.TextField('作业描述', max_length=500, blank=True, null=True)
    scoring_point = models.TextField('得分点', max_length=300, blank=True, null=True)
    re_class = models.ForeignKey('ClassList', verbose_name="班级")
    teacher = models.ForeignKey('UserProfile', verbose_name="讲师", related_name='t_course_record')
    recorder = models.ForeignKey('UserProfile', verbose_name="记录者", related_name='r_course_record')

    class Meta:
        unique_together = ('re_class', 'day_num')


class StudyRecord(models.Model):
    """
    学习记录
    """

    attendance = models.CharField("考勤", choices=attendance_choices, default="checked", max_length=64)
    score = models.IntegerField("本节成绩", choices=score_choices, default=-1)
    homework_note = models.CharField(max_length=255, verbose_name='作业批语', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField("备注", max_length=255, blank=True, null=True)
    course_record = models.ForeignKey('CourseRecord', verbose_name="某节课程")
    student = models.ForeignKey('Customer', verbose_name="学员")

    class Meta:
        unique_together = ('course_record', 'student')

```

# 2. 展示页面

## 2.1 `__str__`方法

1. str方法**必须有返回值**，否则会报错

```python
# 用户信息的 model
class Customer(models.ModelForm):   
  	def __str__(self):
        if self.name:
            return self.name
        return 'None'
```

## 2.2 `__init__`方法

1. 在forms类中使用**初始化方法**
2. 一般重写初始化方法时，需要使用父类的**init**方法

```python
# forms.py
class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields.values():
            if not isinstance(i, (MultiSelectFormField, DateField)):
                i.widget.attrs['class'] = 'form-control'
                print(i, type(i))
            if isinstance(i, DateField):
                i.widget = forms.TextInput(attrs={'placeholder': "YYYY-MM-DD", 'autocomplete': "off", 'type': 'date'})
```

## 2.3 模版文件

1. 此时的字段对象是BoundField对象，其中self.field = field。
2. for 循环中的对象不是原来的**field**
3. 有for循环的一般都有`__iter__`方法
4. self['name'] 会触发`__getitem__`方法
5. 通过判断字段的错误字典，定义显示样式

```django
{# ModelForm通过for循环生成各个字段 #}
{% for i in obj %}
	<div class="form-group col-sm-3"  style="text-align: right">
    	<label for="{{ i.id_for_label }}"
               {% if not i.field.required %}style="color:#8f8f8f"{% endif %}>{{ i.label }}:
        </label>
	</div>
<div class="form-group col-sm-7 {% if i.errors %}has-error{% endif %}"{% if not i.field.required %} style="color:#8f8f8f"{% endif %}>
    {{ i }}
    <span class="help-block">{{ i.errors.0 }}</span>
</div>
{% endfor %}
```

## 2.3 自定义方法

1. 后端处理好html标签样式之后作为字符串传递到前端，需要使用**mark_safe()**标记
2. 如果ModelForm中使用choices=((1, '男'),(2, '女'))，后端处理需要使用`对象.get_字段名_display()`方法，前端使用`对象.get_字段名_display`

```python
    def show_status(self):
        info = {'signed': 'green', 'unregistered': 'red', 'studying': 'skyblue', 'paid_in_full': 'gold'}
        return mark_safe('<span style="color:white; background-color: {};padding:5px">{}</span>'.format(info.get(self.status), self.get_status_display()))
```

## 2.4 中间件处理请求

1. 需要对**admin**账户，**以及登陆**放行
2. 如果后续需要使用一些数据，可以在通过验证之后，把数据封装到**request**对像中，即**reques.变量名 = 值**

```python
# crm.middlewares下的middleware.py
# 登陆校验
class CheckLogin(MiddlewareMixin):
    def process_request(self, request):
        url = request.path_info
        if url in [reverse('login'), reverse('reg')]:
            return
        if url.startswith('/admin'):
            return
        user = request.session.get('is_login')
        if not user:
            return redirect(reverse('login') + '?return_url={}'.format(url))
        obj = models.UserProfile.objects.filter(pk=request.session.get('user_id')).first()
        if obj:
            request.user_obj = obj
```

## 2.5 共用一个html文件

- 路由设计

```python
# urls.py
# 网址不同，经由一个view函数处理
url(r'^add_customer/', views.modify_customer, name='add_customer'),
url(r'^edit_customer/(\d+)', views.modify_customer, name='edit_customer'),
```

- 共用views函数

```python
# views.py
def modify_customer(request, pk=None):
    user_obj = models.Customer.objects.filter(pk=pk).first()
    obj = CustomerForm(instance=user_obj)
    if request.method == 'POST':
        obj = CustomerForm(data=request.POST, instance=user_obj)
        if obj.is_valid():
            obj.save()
            return redirect('show_customer')
    title = '修改客户' if pk else '新增客户'
    return render(request, 'modify_customer.html', {'obj': obj, 'title': title})
```

1. form_obj = CustomerForm(**data**=request.POST, **instance**=user_obj)
   - data表示实例化需要的数据，instance表示html页面渲染用的数据，默认为None

# 3. 公私户转换

1. 使用反射处理多个功能
2. django模版中的，一个标签内部不能再嵌套标签
3. form不能进行嵌套，pull-right/ float

```python
form 表单类型 class='form-inline'
select class='form-control'
```

# 4.模糊查询

## 1. Q查询

```python
q = Q()                                       	# 默认不可更改
q.connector = 'OR'								# 连接条件为 'OR'
q.children.append(Q(qq__contains='查询关键词')) 	 # children方法，类似列表
Q(qq__contains=query)                         	# Q查询条件格式
Q(('qq__contains',query))   					# 通过字符串方式，生成Q条件
# 示例，可以运用到类中
def search(field_list):
  	query = request.GET.get('query', '')
  	q = Q()
    q.connector = 'OR'
    # 方法一
    q.children.append(Q(qq__contains=query))
    ...
    # 方法二
    for i in field_list:
        q.children.append(Q(('{}__contains'.format(i), query)))
        return q
q = search(['qq', 'name', 'phone'])
```

# 5. 分页保留搜索条件

## 1. request.GET的类型

- querydict类型，默认为不可变类型(**修改mutable**)
- urlencode()方法

```python
request.GET   <class 'django.http.request.QueryDict'>   'query': ['13']  
request.GET.urlencode()                 # 对URL进行编码如：query=13&page=1
request.GET._mutable = True             # 可编辑，默认为False，即不可编辑
request.GET.copy()                      # 深拷贝，可编辑
QueryDict(mutable=True)                 # 可编辑
```

## 2. request.GET记录条件

```django
{# 展示页面, 向展示页面发送表单 #}
<form action="" class="form-group" style="float:right">
		<input type="text" name="query" class="btn" style="border-color: silver">
		<button class="btn btn-info">搜索</button>
</form>
```

## 3. 分页器url 拼接搜索条件

```python
# self.params为querydict类型，默认None
self.pararms['page'] = i
li_li.append('<li><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))
```

# 6. 编辑后返回源界面

- 使用get_full_path()方法获取，源界面的路径，作为参数拼接到编辑的url中

## 1. 自定义simple_tag

```python
# 自定义simple_tag
from django.http.request import QueryDict
from django.template import Library
from django.urls import reverse
register = Library()

@register.simple_tag
def reverse_url(request, name, *args, **kwargs):
    next = request.get_full_path()
    url = reverse(name, args=args, kwargs=kwargs)
    qd = QueryDict(mutable=True)
    qd['next'] = next
    return '{}?{}'.format(url, qd.urlencode())
```

## 2. 编辑按钮

- 通过自定义的simple_tag，**获取编辑前的url**

```django
{# 展示页面 #}
{% load my_tags %}
<a href="{% reverse_url request 'edit_customer' i.pk %}">
		<button type="button" class="btn btn-info">修改</button>
</a>
```

# 7. 限制条件

1. 表单发送请求时，get方法会改变url的参数，**原来的参数会被当前form表单的健值对替换**
2. post请求时，不该变url参数
3. querydict中的**urlencode**方法会对**& / = ?** 都会进行编码 

## 1. view函数

- 使用实例化的方式进行参数的传递

```python
# 通过实例化，进行参数的间接传递
def modify_consult(request, pk=None, customer_id=None):
    user_obj = models.ConsultRecord(consultant=request.user_obj, customer_id=customer_id) if customer_id else models.ConsultRecord.objects.filter(pk=pk).first()
    obj = ConsultRecord(instance=user_obj)
    if request.method == 'POST':
        obj = ConsultRecord(data=request.POST, instance=user_obj)
        if obj.is_valid():
            obj.save()
            url = request.GET.get('next', '')
            return redirect(url if url else 'consult_record')
    title = '修改记录' if pk else '新增记录'
    return render(request, 'form.html', {'obj': obj, 'title': title, })
```

## 2. ModelForm类

### 2.1 样式类

```python
# forms.py
# 自定义bootstrap样式类，其他modelform类，继承样式类
class BSForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields.values():
            if not isinstance(i, (MultiSelectFormField, DateField, BooleanField)):
                i.widget.attrs['class'] = 'form-control'
            if isinstance(i, DateField):
                i.widget = forms.TextInput(attrs={'placeholder': "YYYY-MM-DD", 'autocomplete': "off", 'type': 'date'})
```

### 2.2 条件限制	

1. 自定义其他modelform类，通过`__init__`方法进行，self.fields为有序字典
2. 列表的相加、列表生成式
3. self.fields['**外键**'].choices , 类型为 **<class 'list'>** ，值的格式为`[(20, <Customer: oleg1>), ...]`

```python
# forms.py
# 通过自定义，__init__方法，获取当前销售对象，以及当前客户信息
class ConsultRecordForm(BSForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ConsultRecord, self).__init__(*args, **kwargs)
        # 如果id为 0， 则表示新增任意客户的跟进记录
        # 不为0，则表示新增当前客户的跟进记录
        if self.instance.customer_id != '0':
            self.fields['customer'].choices = [(self.instance.customer.pk, self.instance.customer.name)]
        else:
            self.fields['customer'].choices = [('', '-------------')] + 
                [(i.pk, str(i)) for i in self.instance.consultant.customers.all()]
        # 限制为当前销售
        self.fields['consultant'].choices = [(self.instance.consultant.pk, self.instance.consultant)]
```

- 在实例化时，通过参数进行传递，注意执行super方法时的参数

```python
def __init__(self, request, customer_id, *args, **kwargs):
    super(ConsultRecord, self).__init__(*args, **kwargs)
    if customer_id and customer_id != '0':
      	self.fields['customer'].choices = [(i, str(i)) for i in models.Customer.objects.filter(pk=customer_id)]
    else:
        self.fields['customer'].choices = [('', '-------------')] + [(i.pk, str(i)) for i in request.user_obj.customers.all()]
    # 限制为当前销售
		self.fields['consultant'].choices = [(request.user_obj.pk, request.user_obj)]
```

#### Note

1. **本质**：通过参数的传递，经由orm操作帅选，并把字段对象的choices参数进行替换

# 8. django开启事务

## 8.1 djano使用行级锁

```python
from django.db import transaction
 
try:
  	with transaction.atomic():
      	# orm操作
        queryset = models.类.objects.filter(pk__range=[1,3]).select_for_update()
        queryset.update(字段=值)
except Exception as e:
  	print(e)
```

## 8.2 mysql使用行级锁

```mysql
begin;				# 开启事务
# 添加行级锁
select * from t1 where id=1 for update;
# 增删改操作
commit;				# 结束事务
```

## 8.3 全局变量

```python
# settings.py
MAX_CUSTOMER_NUM = 150  # 配置写大写
```

- 使用Django.conf导入时，**变量名必须大写**
- django把默认配置和settings里的数据封装在了一起

```python
# views.py
from app.settings import MAX_CUSTOMER_NUM
# 或者
from django.conf import settings
settings.MAX_CUSTOMER_NUM
```

# 9. modelformset

```python
# 导入
from django.forms import modelformset_facotry
# 实例化一个formset对象
ModelFormSet = modelformset_factory(models.类, ModelForm类, extra=0)
# 绑定数据，并使用对象进行填充
form_set_obj = ModelFormSet(queryset=orm查询)
# 绑定数据，提交更新后数据
form_set_obj = ModelFormSet(queryset=orm查询, date=request.POST)
if form_set_obj.is_valid():
  	form_set_obj.save()
```

- 模版中使用

```django
{# 编辑相关，只要是提交post表单就需要生成4个隐藏标签 #}
{{ form_set_obj.management_form  }}

{# form为循环出来的一个form表单对象,指定字段为不可变类型 #}
{{ form.instance }}         {# 当前form对象 #}
{{ form.instance.username }}  
{# 循环出来的input/select框 #}
{{ form.username }}

{# 循环内部需要生成form表单的id #}
{{ form.id }}
```

```python
modelformset_factory() uses formset_factory() to generate formsets. This means that a model formset is just an extension of a basic formset that knows how to interact with a particular model.
# modelformset_factory()使用formset_factory()生成formsets，model formset是基于formset的延伸。
```

# 10. 权限组件  

## 1. 权限

1. 让不同的人使用不同的功能

2. **开发一个权限的组件**
  
   - 实现一个完整功能
   
   - 提高开发效率，可以重复使用**权限组件**
   
3. web开发中的权限就是：**url代表权限**

4. 表结构设计(基础功能)
   1. 用户表user：id username pwd role_id
   2. 权限表：permission
      - id url title
   3. **用户-权限关系表**：id role_id permission_id
   4. 角色表：id name 
   5. **用户-角色表** ：id user_id role_id

5. **RBAC**：**role-base access contorl**

### 1.1 创建rbac app

```python
# models.py
class Permssion(models.Model):
    url = models.CharField('url', max_length=150)
    title = models.CharField('标题', max_length=32)
    def __str__(self):
       	return self.title

class Role(models.Model):
  	name = models.CharField('角色', max_length=32) 
    permssions = models.ManyToManyField('Permisson', verbose_name='角色拥有的权限', blank=True)
    def __str__(self):
       	return self.name
    
class User(models.Model):
  	username = models.CharField('用户名', max_length=32)
    pwd = models.CharField('密码', max_length=32)
    roles = models.ManyToManyField('Role', verbose_name='用户角色', blank=True)
    def __str__(self):
       	return self.username
```

- 数据库迁移(使用sqlite3)，文件型数据库

- 实则5张表

  

## 2. admin插入数据

- id**是不可编辑的**

```python
# admin.py
from django.contrib import admin
from rabc import models
class PermissionConf(admin.ModelAdmin):
  	# 展示多列
  	list_display = ['id', 'url', 'title']
    # 可编辑的，id是django自动生成的，不可以更改
    list_editable = ['url', 'title']
admin.site.register(models.Permission, PermissionConf)
```

- session可以存放到其他位置
- 查询权限

```python
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = models.User.objects.filter(username=username, password=password).first()
        if obj:
            # 登陆成功, 初始化登陆状态、权限和菜单的seesion信息
            init_session(request, obj)
            return redirect('index')
    return render(request, 'login.html')
# 添加session
permissions = user_obj.roles.filter(permission_url__is_null=False).values('permission_url')
# 保存到session，放入session中的数据，会json序列化，并加密存储
request.session['permissions'] = list(permissions)
```

- **白名单使用正则表达式**：re.match(正则, 字符串)
- 登陆状态、index、权限验证

## 3. 使用inclusion_tag生成菜单

```python
from django.template import Library
import re

register = Library()
@register.inclusion_tag('menu.html')
def menu(request):
    menu_list = request.session.get('menu_list')
    url = request.path
    for i in menu_list:
        if re.match(r'{}$'.format(i['permissions__url']), url):
            i['class'] = 'active'
            break
    return {'menu_list': menu_list, 'request': request}
```

# 11. 菜单和breadcrump

## 1. 一级菜单的排序

1. dict在3.6 是无序的，显示有序，3.7之后是有序的
2. 有序菜单(有序字典)
3. 给菜单加优先级
4. 使用有序字典，先排序后构造

### 1.1 models.py

```python
# model.py，优先级设置最好有些跨度
class Menu(models.Model):
    title = models.CharField('标题', max_length=32)
    icon = models.CharField('图标', max_length=100, null=True, blank=True)
    weight = models.IntegerField('优先级', default=1)

    def __str__(self):
        return self.title
```

### 1.2 my_tags.py

- **sorted()**内置函数的应用

```python
# my_tags.py
from collections import OrderDict
@register.inclusion_tag('menu.html')
def generator(request):
  	url = request.path
    menu_dic = request.session.get(settings.MENU_SESSION_KEY)
    od = OrderDict()
    # 排序，结果只有字典的 key
    keys = sorted(menu_dic, key=lambda x:menu_dic[x]['wight'] ,reverse=True)
    for i in keys:
        od[i] = menu_dic[i]
    
    for i in menu_dic.values():
      	i['class'] = 'hide'
      	for m in i['children']:
          	re.match(r'{}$'.format(m['url']), url)
            m['class'] = 'active'
            i['class'] = ''
    return {'menu_dic':od.values()}
```

### 1.3 二级菜单开合

- js控制的选项卡

```js
// 菜单的点击事件，功能就是“选项卡”
$('.title').click(function () {
    $(this).next().removeClass('hide');
    $(this).parent().siblings().find('.body').addClass('hide')
});
```

## 2. 二级菜单的子菜单

### 2.1 修改models.py

- url 即权限
- menu 外键，表示归属于哪个一级菜单
- parent 自关联外键，表示权限的归属关系(**属于哪一个二级菜单**)

```python
class Permission(models.Model):
    url = models.CharField('路径', max_length=100)
    title = models.CharField('标题', max_length=32)
    menu = models.ForeignKey('Menu', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return self.title
```

### 2.2 session的初始化(重点)

- 构造权限字典和菜单字典
- 需要权限的**id**和自关联外键parent，表明归属
- 菜单字典：键**children**需要当前**id**，**用于和当前权限的归属做判断**

```python
# init_session.py
from django.conf import settings
def init_session(request, obj):
    request.session['is_login'] = True
    permissions = obj.roles.exclude(permissions__url__isnull=True).values(
       # url和title用于菜单标题和链接
        'permissions__url',
        'permissions__title',
        # 菜单相关
        'permissions__menu__icon',
        'permissions__menu__title',
        'permissions__menu_id',      # 二级菜单关联的外键
        'permissions__menu__weight', # 优先级，用于对一级菜单的排序
        # 二级菜单的子菜单，和面包屑
        'permissions__parent_id',
        'permissions__id',
    ).distinct()

    # 构造权限和菜单的字典
    permission_dic = {}
    menu_dic = {}
    for i in permissions:
        permission_dic[i['permissions__id']] = {
       			# url和title用于菜单标题和链接
            'url': i.get('permissions__url'),
            'title': i.get('permissions__title'),
          	# id 和 pid 用于访问二级菜单中的子菜单时，保持二级菜单处于活跃状态
            'id': i.get('permissions__id'),
            'pid': i.get('permissions__parent_id'),
        }
        
        menu_id = i.get('permissions__menu_id')
        if menu_id:
            if not menu_dic.get(menu_id):
                menu_dic[menu_id] = {
                    'title': i.get('permissions__menu__title'),
                    'icon': i.get('permissions__menu__icon'),
                    'weight': i.get('permissions__menu__weight'),
                    'children': [
                        {'title': i.get('permissions__title'),
                         'url': i.get('permissions__url'),
                         'id': i.get('permissions__id'),
                         }]}
             else:
                menu_dic[menu_id]['children'].append(
                    {'title': i.get('permissions__title'),
                     'url': i.get('permissions__url'),
                     'id': i.get('permissions__id'),
                     })
    # 权限列表
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dic
    # 菜单列表
    request.session[settings.MENU_SESSION_KEY] = menu_dic

```

#### Note

1. 构造数据结构时，首先考虑**dict**类型

### 2.3 获取当前url的归属

- 通过 Middleware 获取，只要接收到请求，就要判别其归属

```python
# 权限校验,中间件
for i in permissions:
  	if re.match(r'{}$'.format(i['url']), path):
        sid = i['id']
        pid = i['pid']
        if pid:
            request.current_menu_id = sid
        else:
            request.current_menu_id = sid
        return 
```

### 2.4 inclusion_tag

- 用于样式的定制和修改

```python
# my_tags.py
from collections import OrderedDict
from django.conf import settings
from django.template import Library

register = Library()
@register.inclusion_tag('menu.html')
def menu(request):
    menu_dic = request.session.get(settings.MENU_SESSION_KEY)
    # print(menu_dic.values())
    # 通过有序字典，为一级菜单指定顺序
    od = OrderedDict()
    keys = sorted(menu_dic, key=lambda x: menu_dic[x]['weight'], reverse=True)
    for i in keys:
        od[i] = menu_dic[i]
    
    # 二级菜单样式
    for i in menu_dic.values():
        i['class'] = 'hide'
        for m in i['children']:
            # print(m['id'])
            if request.current_menu_id == m['id']:
                m['class'] = 'active'
                i['class'] = ''
    return {'menu_dic': od}
```

## 3. 路径导航(breadcrumb)

- 添加父权限导航
  - 数据库查询
  - pid 循环字典
  - **改变数据结构**

### 3.1 通过中间件构造 breadcrumb_list

- django在存储session时，会自动进行序列化和加密，data中的数字不受影响
- json序列化时，字典中的**key**为数字为时，会变成字符串，反序列化后还是字符串
- dict本质是一张hash表

```python
for i in permission_dic.values():
  	# print(permission_dic.values())
  	# 二级菜单的匹配
  	if re.match(r'{}$'.format(i.get('url')), path):
    		sid = i.get('id')
    		pid = i.get('pid')
        # print(sid, pid)
        # current_menu_id，当前url的对应的二级菜单的id
        if pid:
              # 当前访问子权限
              request.current_menu_id = pid
              # 路径导航，注意此时的数字key 是字符串
              request.breadcrumb_list.append({'title': permission_dic[str(pid)]['title'], 'url': permission_dic[str(pid)]['title']})
              request.breadcrumb_list.append({'title': i['title'], 'url': i['url']})
          else:
                # 当前访问父权限(二级菜单)
                request.current_menu_id = sid
                # 路径导航
                reqsuest.breadcrumb_list.append({'title': i['title'], 'url': i['url']})
          return
```

### 3.2 my_tags.py和breadcrump.html

#### 1. my_tags.py

```python
@register.inclusion_tag('breadcrumb.html')
def breadcrumb(request):
    return {'breadcrumb_list': request.breadcrumb_list}
```

#### 2. Breadcrump.html

- breadcrumb样式在bootstrap中

```django
<ol class="breadcrumb no-radius no-margin" style="border-bottom: 1px solid #ddd;">
    {% for breadcrumb in breadcrumb_list %}
        {% if forloop.last %}
            <li class="active">{{ breadcrumb.title }} </li>
        {% else %}
            <li><a href="{{ breadcrumb.url }}">{{ breadcrumb.title }}</a></li>
        {% endif %}
    {% endfor %}
</ol>
```

# 12. rbac组件应用

1. 拷贝rbac组件到新项目中，并注册

   ```python
   INSTALLED_APPS = [
   		...
       'rbac.apps.RbacConfig'
   ]
   ```

2. 数据库迁移

   1. 修改用户表

      ```python
      class User(models.Model):
          """用户表"""
          # username = models.CharField('用户名', max_length=32)
          # password = models.CharField('密码', max_length=32)
          roles = models.ManyToManyField(Role, verbose_name='用户所拥有的角色', blank=True)
      	# 多对多关联写成类  不写字符串
          class Meta:
              abstract = True  # 数据库迁移时不生成表  作基类 继承使用
      ```

   2. 新项目的用户表继承User

      ```python
      from rbac.models import User
      class UserProfile(User):
      ```

   3. 执行数据库迁移的命令

      1. 先删除rbac中migrations中的除了init之外的py文件

      2. 执行 

         python manage.py makemigrations

         python manage.py migrate

3. 路由配置

   ```python
   urlpatterns = [
    	....
       url(r'^rbac/', include('rbac.urls')),
   ]
   ```

4. 角色管理

   <http://127.0.0.1:8000/rbac/role/list/>

5. 一级菜单管理

   <http://127.0.0.1:8000/rbac/menu/list/>

6. 批量操作权限

   <http://127.0.0.1:8000/rbac/multi/permissions/>

   批量输入标题

   给权限分配给一级菜单  给父权限分配子权限

7. 分配权限

   如果用的不是rbac的User，替换User为当前使用的用户model

   给角色分权限

   给用户分角色

8. 应用权限的中间件

   ```python
   MIDDLEWARE = [
   	...
       'rbac.middlewares.middleware.AuthMiddleWare',
   ]
   ```

   在settings中添加权限的配置

   ```python
   #  白名单
   WHITE_LIST = [
       r'/login/$',
       r'/reg/$',
       r'/admin/.*'
   ]
   
   # 免认证的地址
   NO_PERMISSION_LIST = [
       r'/index/'
   
   ]
   
   # 权限的session的key
   PERMISSION_SESSION_KEY = 'permission'
   
   # 菜单的session的key
   MENU_SESSION_KEY = 'menu'
   ```

   登录成功后调用权限信息初始化的函数

9. 动态生成二级菜单

   ```django
   {% load rbac %}
   {% menu request %}
   ```

	使用 css js
	
	```python
	# css
	<link rel="stylesheet" href="{% static 'css/nav.css' %} "/>
	# js
	<script src="{% static 'rbac/js/menu.js' %} "></script>
	```

10. 路径导航

    ```django
    {% breadcrumb request %}
    ```

11. 权限控制到按钮级别

    ```python
    {% load rbac %}
    {% if request|has_permission:'add_consult' %}
           <a href="{% url 'add_consult' customer_id %}" class="btn btn-primary">新增</a>
    {% endif %}
    ```

    









































# 附录：

## 1. Django中模块的导入

### 1.1 form组件相关(3)

```python
# form 组件的导入
from django import forms
# form校验的异常导入
from django.core.exceptions import ValidationError
# MultiSelectFormField, 第三方模块，pip3 install django-multiselectfield
from multiselectfield.forms.fields import MultiSelectFormField
```

### 1.2 URL相关(1)

```python
# url配置，路由分发，路由的反解析
from django.conf.urls import url, include
```

### 1.3 Model相关(4)

```python
# 对象关系映射模型
from django.db import models
# 聚合分组相关，以及 F，Q查询
from django.db.models import F, Q, Max, Min, Avg, Count, Sum
# 事务
from django.db import transcation
# 自定义方法中的 html 标签，在进行不转义显示
from django.utils.safestring import mark_safe
```

### 1.4 Template相关(2)

```python
# 导入模版
from django import template
register = template.Library()
# html标签取消转义
from django.utils.safestring import mark_safe
```

### 1.5 View相关(5)

```python
# 导入视图
from django.views import View
# 响应以及路由的反解析
from django.shortcuts import render, redirect, HttpResponse, reverse
# HttpResponse的导入
from django.http import HttpResponse
# JsonResponse的导入, 通常用于dict类型，如果是list，需要指定safe=False， 默认为True
from django.http.response import JsonResponse
		return HttpResponse(data，content-type = 'applicatoin/json')
# querydict 类
from django.http.request import QueryDict
# 模版的响应
from django.template.response import TemplateResponse
```

### 1.6 装饰器相关(2)

```python
# 给CBV加装饰器
from django.utils.decorators import method_decorator
# csrf中的装饰器
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
```

### 1.7 中间件相关(1)

```python
from django.utils.deprecation import MiddleMixin
```

### 1.8 admin相关(2)

```python
from django.contrib import admin
from app import models
admin.site.register(models.UserProfile)
```

### 1.9 app相关(1)

```python
from django.app import AppConfig
class App01Config(AppConfig):
		name='app01'
```

## 2. 其他

### 2.1 form表单错误

```django
{{ form_obj.non_field_errors.0 }}        {# 错误信息存放在__all__中 #}
```

### 2.2  static查找顺序

- 按照app的注册顺序进行查找，一旦找到即结束(**命名不能相同**)
- STATICFILES_DIRS是项目目录下的静态文件，app会自动查找不用配置







