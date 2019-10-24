# nginx

-   是个web服务器、常用作静态文件服务器、常用作负载均衡。
-   nginx是个web服务器,常用作静态文件服务器，反向代理服务器,邮件代理服务器,负载均衡服务器。

## 0. 虚拟环境

### 1. 安装

```pythom
pip install virtualenv -i https://pypi.douban.com/simple
```

### 2. 新建

```shell
# 新建到当前文件夹，虚拟环境为 test-env
virtualenv --no-site-packages --python=python3 test-env
```

-   安装`virtualenvwarpper`

```shell
pip install virtualenvwarpper
workon
# 会有默认路径
mkvirtualenv -p python3 test
# 进入虚拟环境
workon 虚拟环境名 
```

## 1. 安装、配置文件

### 1. 安装

```shell
# 安装淘宝nginx,编代码编译安装,先解决模块依赖
yum install gcc patch libffi-devel python-devel  zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel openssl openssl-devel -y
```

```shell
# 获取淘宝nginx的源代码
wget http://tengine.taobao.org/download/tengine-2.3.2.tar.gz
# 解压缩源代码包
tar -zxvf tengine-2.3.2.tar.gz
```

```shell
# 进入源代码目录开始编译三部曲
1. 指定安装路径
	./configure --prefix=/opt/tngx

2.编译且安装
	make && make install 

3.安装完成之后,进入nginx的目录,
	[root@localhost tngx]#pwd
	/opt/tngx
	[root@localhost tngx]#ls
	conf  html  logs  sbin
	
	# conf 存放配置文件 , 指定了这个软件各种功能的一个文件而已  
	# html 存放前端页面
	# logs nginx的运行日志
	# sbin  nginx的可执行命令目录
	
4.进入sbin目录,启动nginx
    ./nginx  
    ./nginx -s stop 停止nginx
    ./nginx -t  检查nginx.conf的语法是否正确
    ./nginx -s reload  不重启nginx,重新加载nginx配置
```

### 2.  配置文件学习

-   这里的所有配置是nginx的核心功能
-   找到nginx.conf,学习语法

#### 1. nginx核心功能

```shell
http {

    # nginx访问日志功能
    log_format
    access_log
    # gzip 压缩，节省带宽资源
    gzip on
    # nginx支持多虚拟主机，只需写入多个server关键字
    # 虚拟机1
    server {
		...
    }
    # 虚拟机2
    server {
		...
    }
}
```

#### 2. 访问日志

```shell
http {
    include       mime.types;
    default_type  application/octet-stream;
	# 日志格式化
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
                      
	access_log  logs/access.log  main;       
	....
}
```

#### 3. 虚拟主机配置

```shell
http {
    # nginx支持多虚拟主机,只需要写入多个server关键字即可
    # 虚拟主机1
    server {
        # 基于端口的虚拟主机区分 
        listen       80;
        # 基于域名的虚拟主机区分
        server_name  www.test.com;
        # charset koi8-r;
        # access_log  logs/host.access.log  main;
        # access_log "pipe:rollback logs/host.access_log interval=1d baknum=7 maxsize=2G" main;
        # 这里是nginx的url匹配,如同django的url规则一样
        # 当我的请求时 http://172.16.44.142:81/test.jpg  这样的时候,就进入如下location匹配
        # 这个是最低级的匹配,所有请求都会走到这里
        location / {
            # root关键字定义虚拟主机的根目录, 这里是可以修改的
            root   /opt/test/;
            # 必须保证首页文件存在，index参数是定义首页文件的名字的
            index  index.html index.htm;
        }
	}

# 虚拟主机2 
server {
		listen       80;
		server_name  www.henry.com;
		location / {
			root   /opt/henry/;
			index  index.html index.htm;
		}
	}
}
```

#### 4. 错误页面404优化

```shell
server {
    listen 80;
    # 通过这个参数定义即可
    error_page  404   /404.html;
    location / {
    	# 指定 404.html页面的文件目录
        root   /opt/404;
        index index.html;
    }
}
```

#### 5. nginx反向代理

```shell
# 代理
# 用户,客户端    中介,代理服务器,   房东,资源服务器
# 租房的客户  ->  中介,代理  ->   房东 
# 浏览器 -> nginx  ->  django 

环境如下
机器1 	172.16.44.142  是代理服务器的角色，nginx提供的功能
机器2		172.16.44.143  是资源服务器的角色，nginx静态资源服务器
```

-   反向代理服务器配置如下

```python
# 打开172.16.44.142 机器的nginx.conf,修改为如下
server {
    listen       80;
    server_name  www.test.com;
    location / {
        # root   /opt/test/;
        # index  index.html index.htm;
        # 实现反向代理的功能参数
        proxy_pass http://172.16.44.143;
    }
}
```

#### 6. nginx负载均衡

```shell
# 环境准备
1台负载均衡服务器，nginx而已     172.16.44.142 是负载均衡服务器
2台资源服务器  
```

```shell
# 准备好2台资源服务器,本应该提供一样的数据,进行负载均衡,实验目的,看到不同的页面,所以准备不同的页面数据
	172.16.44.142  资源服务器1，返回 test 的页面 
	172.16.44.143  资源服务器2，返回 henry 的页面
```

-   默认轮询方式

```python
# 准备负载均衡服务器,配置如下
# 在nginx配置文件中,添加如下配置,定义负载均衡池,写入后端项目地址
upstream mydjango  {
    server 172.16.44.142;
    server 172.16.44.143;                                                                    
}
```

-   权重方式

```shell
# 权重方式
upstream mydjango  {
	server 172.16.44.142	weight=4;
	server 172.16.44.143	weight=1;                                                                    
}
```

-   ip地址hash方式

```python
# ip哈希方式,根据用户的来源ip计算出哈希值,永远只指派给一个服务器去解析
# ip哈希不得与权重共同使用 
upstream mydjango  {
    server 172.16.44.142;
    server 172.16.44.143;         
    ip_hash;
}
```

```shell
# socket协议请求的负载池
# upstream myvue{
#         server 172.16.44.142:8888 weight=10;
#         server 172.16.44.143:8888 weight=1; 
# }

#虚拟主机配置如下
server {
    listen       80;
    server_name  www.test.com;
    location / {
        proxy_pass http://mydjango;
        # socket进行负载均衡
        # uwsgi_pass myvue;
    }
}
```

## 3. 项目部署

### 1. nginx + uwsgi + django + mysql 

```shell
# 上传crm项目到linux服务器
# 安装uwsgi命令，这是python的一个模块
# 激活一个虚拟环境去使用

virtualenv --no-site-packages --python=python3   uwsgi_django
pip3 install -i https://pypi.douban.com/simple  uwsgi 

pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple django==1.11.23
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pymysql 
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple django-multiselectfield
```

### 2. 启动  crm项目

-   使用uwsgi的命令，参数形式

```shell
# 以往的python3 manage.py runserver 调用wsgiref去启动django,性能很低,单进程web
# 使用uwsgi启动django,可以支持并发,多进程,以及日志设置,多种功能

# 必须在django项目,第一层敲这个命令
uwsgi --http :8000 --module henry_crm.wsgi
	--http 指定是http协议,去启动项目
	--module  指定django目录下的wsgi文件
# uwsgi支持的热加载命令
uwsgi --http :8000 --module henry_crm.wsgi   --py-autoreload=1 
```

-   测试

```python
# 需要清空防火墙规则
iptables -F
```

### 3. uwsgi配置文件启动 

-   把启动参数，写入到一个文件中，然后执行这个文件即可
-   配置文件名字可以叫做 uwsgi.ini ，内容如下，这个文件是手动生成的

```shell
touch uwsgi.ini ,写入如下内容

[uwsgi]
# Django-related settings
# the base directory (full path)
# 填入项目的绝对路径，项目的第一层路径
chdir           = /opt/projects/henry_crm
# Django's wsgi file
# 指定第二层项目下的wsgi文件
module          = henry_crm.wsgi
# the virtualenv (full path)
# 找到虚拟环境的绝对路径
home            = /opt/projects/env/crm_env
# process-related settings
# master
master          = true
# 以cpu核数来填写，uwsgi的工作进程数
processes       = 2
# the socket (use the full path to be safe
# 这是以uwsgi_socket协议启动的项目，无法再去通过浏览器访问，必须通过nginx以uwsgi协议去反向代理
socket          = 0.0.0.0:8000
# 也可以使用http协议去启动(仅用作调试使用)
# http = 0.0.0.0:9000
# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum          = true
# 后台运行参数,将uwsgi运行在后台,并且将django日志输出到uwsgi.log中
daemonize = uwsgi.log 
```

### 4. 指定配置文件启动django

```shell
uwsgi --ini  uwsgi.ini
```

## 4. 配置反向代理

### 1. 修改nginx.conf如下

```shell
server {
    listen       80;
    server_name  www.test.com;
    location / {
        # 转发请求的方式配置在这里
		include    uwsgi_params;
		uwsgi_pass 0.0.0.0:8000;
    }
}
```

### 2. 重新加载nginx,

-   访问nginx，查看是否反向代理
-   用浏览器访问nginx的地址，查看能否访问到crm的内容

### 3. 收集crm的静态文件

-   丢给nginx去解析
-   对django的settings.py配置修改如下

```shell
# 添加如下参数
STATIC_ROOT='/opt/crm_static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
	os.path.join(BASE_DIR, 'static')
]
# 执行命令,收集django的所有静态文件,系统会自动创建'/opt/static'  这个文件夹
python3 manage.py collectstatic
```

### 4. 配置nginx

-   找到crm的这些静态资源

```shell
location / {
    include    uwsgi_params;
    uwsgi_pass 0.0.0.0:8000;
}
       # 添加一个location,针对nginx的url进行匹配处理
       # 当请求时 www.oldchouhuo.com/static/.....  这样的url的时候,nginx进行别名修改,去/opt/s21static底下去寻找资源文件                                                                                                                          
location  /static {
	alias /opt/static;
}

# 此时再次访问网站,查看是否处理了静态资源
www.test.com
```

## 5. 前后端分离的部署笔记

### 1. 后端部署

-   uwsgi + drf + redis + mysql 

#### 1. 准备后端代码

```python
# 下载测试代码
wget https://files.cnblogs.com/files/pyyu/luffy_boy.zip
```

#### 2. 创建且激活新的虚拟环境

```python
# 创建虚拟环境
virtualenv --no-site-packages --python=python3
```

#### 3. 解决模块依赖问题,尝试调试启动drf后台

```shell
[root@localhost opt]# cat requirements.txt
	certifi==2018.11.29
	chardet==3.0.4
	crypto==1.4.1
	Django==2.1.4
	django-redis==4.10.0
	django-rest-framework==0.1.0
	djangorestframework==3.9.0
	idna==2.8
	Naked==0.1.31
	pycrypto==2.6.1
	pytz==2018.7
	PyYAML==3.13
	redis==3.0.1
	requests==2.21.0
	shellescape==3.4.1
	urllib3==1.24.1
	uWSGI==2.0.17.1
pip3 install -i https://pypi.douban.com/simple -r requirements.txt
```

#### 4. 使用uwsgi,启动drf后台

```shell
touch uwsgi.ini
[uwsgi]
chdir           = /opt/projects/luffy_boy
module          = luffy_boy.wsgi
home            = /opt/env/uwsgi_vue
master          = true
processes       = 2
socket          = 0.0.0.0:8000
vacuum          = true
daemonize = uwsgi.log
```

### 2. 前端部署

#### 1. 下载前端vue代码

```shell
wget https://files.cnblogs.com/files/pyyu/07-luffy_project_01.zip
# vue+nginx的端口	  80端口，使用 server_name = www.vue.com
# nginx反向代理端口	9000   这是第二个虚拟主机
# 业务逻辑drf的后台端口  	 8888 
```

#### 2. 访问步骤

```shell
第一步: 172.16.44.142:80  查看到路飞的首页内容,是vue的静态页面
第二部: 点击课程列表的时，vue向后台发送请求了，发送的地址应该是 172.16.44.142:9000
第三部: 此时  nginx的反向代理,转发请求给了 drf的后台 8888
# 修改vue的请求发送地址,重要!!!!，修改vue请求地址,向服务器的ip地址发送请求
# sed 使用语法
sed -i  "s/127.0.0.1:8000/172.16.44.142:9000/g"  src/restful/api.js 
	-i 将替换结果写入到文件
	"s/你想替换的内容/替换之后的内容/g"      s是替换模式  g是全局替换 
```

#### 3. 安装nodejs编译vue代码

```shell
# 配置nodejs的解释器环境,打包编译vue代码,生成静态文件夹dist
# 这里的node代码包,是二进制包,已经编译好了,可以直接使用
wget https://nodejs.org/download/release/v8.6.0/node-v8.6.0-linux-x64.tar.gz

# 解压缩node的代码包
tar -zxvf node-v8.6.0-linux-x64.tar.gz 

# 配置PATH环境变量
PATH='/opt/py37/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/opt/tengine/sbin:/opt/node-v8.6.0-linux-x64/bin' 

# 检查node是否可用
[root@localhost bin]# node -v
v8.6.0
[root@localhost bin]# npm -v
5.3.0
```

```shell
# 进入vue代码目录,开始编译代码,生成dist静态文件夹
cd /opt/projects/luffy_vue/
#开始安装这个项目所有需要的node模块,默认去读取 package.json
npm install 
#开始编译vue代码,生成dist静态网页文件夹,丢给nginx 
npm run build 
```

### 3. 在正确生成dist之后，配置nginx 

```shell
# 这里配置和luffy学成有关的代码
# 这个是nginx+vue的虚拟主机
server {
        listen 80; 
        server_name www.myvue.com;
        error_page  404              /404.html;
        # 请求来到这里时,返回vue的页面
        location / { 
            root   /opt/projects/luffy_vue/dist;
            index index.html;
            # 404报错
            try_files $uri $uri/ /index.html;
        }   
    } 
    
# 这个是nginx反向代理,转发vue请求给drf的虚拟主机
server {
         listen 9000;
         server_name localhost;
         location / { 
             include    uwsgi_params;
             uwsgi_pass 0.0.0.0:8888;
         }   
    }   
# 此时访问vue地址即可,看到路飞页面,且可以看到课程列表的数据，可以添加linux，和django的课程，到购物车中，整个部署过程结束
```

### 4. 安装并启动redis



