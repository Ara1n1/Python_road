# AI常用词汇

1.  ASR(automatic speech recongition)：语音识别
2.  TTS：text to speech：语音合成
3.  IR：image recogition：图像识别
4.  NLP：natrural language processing
5.  QPS：query per second 每秒钟允许的请求的次数

护照：世界统一格式

## 1. 语音识别

1.  需要的语音文件为 pcm，wav，amr格式，可以使用 ffmpeg 进行格式转换
2.  pycharm环境变量只在启动加载一次
3.  修改读取文件的函数：os.system的命令

```python
# 执行系统命令
import os, subprocess
res = os.system('ls')
# 0表示成功，1表示失败
print(res)
res = subprocess.Popen('ls')
os.system('xx.mp3')
os.system('ffplay xx.mp3')
```

-   相似度：60%以上就认为是相同的

```python
# 问答机器人-图灵机器人
www.tuling123.com
```

-   request使用get，post发送请求

```python
import requests
res = requests.get('url')
# content为bytes类型，text为utf8文本
print(res.content)
print(res.text)
print(res.json())

res = reqeusts.post(url, json={'k':'v'})
res.json()
```

```python
# 使用ffmpeg进行格式转换
ffmpeg -i test.mp3 -f s16le -ar 16000 -ac 1 -acodec pcm_s16le pcm16k.pcm
```

# 预备知识

## 1. Hbuilder X

-   onclick表示鼠标点击事件
-   tap：表示点击事件
-   release用来结束hold事件

### 1. html的代码块

```css
mdo：构建初始页面，选择css和js，mdocument
mhe：标题栏
mbo：主体，所有代码需要写进此块中
msl：轮播图
mg：九宫格
mli：图文列表
mta：底部选项卡
minput：input框
```

### 2. js代码块

```js
funn			// 创建函数
fori			// for循环
maj				// ajax
mpost			// ajax，post请求
mget			// ajax，get请求
dga				// 为标签绑定事件
```

```js
mui.init();		// 初始化页面参数
mpr				// 初始化h5+
ming			// 初始化手势配置
dga				// 绑定事件，document get by id addEvent
mdt				// 消失的窗口，mtoast
```

-   调用摄像头
-   _doc/camera/：如果没有 / 则代表是文件，会覆盖；当前应用的私有目录

```js
document.getElementById('open').addEventListener('tap', function() {
    mui.toast('open...');
    var cmr = plus.camera.getCamera(1);    // 获得摄像头对象
    res = cmr.supportedImageResolutions[0];// 获得支持的图片分辨率
    fmt = cmr.supportedImageFormats[0];	   // 获得支持的图片格式
    // 调用摄像头
    cmr.captureImage(
        function(s) {
            console.log(JSON.stringify(s));
            console.log('拍照成功');
   		 },
        function(err) {
        	console.log('拍照失败');
    	},
        {
            resolution: res,
            format: fmt
    	})
});
```

### 3. 调用H5+

```js
mui.plusReady(function () {})				// h5+ 加载事件，和h5相关的js操作需要使用
mui.back();									// 返回上一级
document.getElementById('open').addEventListener(tap);
```

```js
// 注册，login页面
1. 创建 html
2. mdo
3. mhe // 带返回箭头的
6. 使用ui组件
7. 给注册按钮绑定事件
```

```js
// index页面
4. 为设置绑定事件(mdt检测事件是否绑定成功)
5. mop	// 打开新页面
```

```js
// 创建reg页面
8. mhe
9. mbo
10.返回按钮：class=mui-action-back
11.注册按钮绑定事件
12.校验密码
13.使用ajax提交post请求，数据提交给Flask
14.mui.ajax/mui.get()/mui.post()
15.mba：返回上一级
16.密码md5加密
17.plus打开系统相册，gallery，uploader
18.使用uploader对象上传文件
```



## 2. 创建userinfo页面

```js
// 返回页面是否有更改后的值
mopen
1. extras
2. styles:{需要bottom，必须有top}
```

```html
<div style="text-align:center">
	<img srt="" style="border-radius:50%; width:200px; height:200px">
</div>
```

```js
// 获取当前页面所有数据
var data = plus.webview.currentWebview();
```

```js
// 重写mui.back函数
mui.back = function(){
    mui.toast('msg')
}
```

```js
// 类似 session/cookies，只能存储字符串类型
Storage
```

## webview

-   主页和首页进行分开加载

```js
加载子页面
入口也不好控制，尽量分开
```

-   存储公共变量：存储url

```js
// js文件
window.serv = "http://192.168.12.4:9527"
window.serv_icon = window.server + '/get_icon/';
```

-   获取其他页面数据

```js
// object类型
var user_info_webview = plus.webview.getWebviewByiId('user_info');
mui.toast(user_info_webview.username);
// 自定义事件：跨页面调度
// 向目标的webview发送指令
mui.fire()
// 获取传递的数据
console.log(eventData.detail)
```

-   使用app录音，将录音发送给web，web收到录音播放

```js
app录音
1. 按住：hold事件和其他事件冲突
2. 按住说话
3. 松开
4. 保存录音
5. 将录音发送 "$出去"，
	uploader发送录音 格式amr
	返回值 t(改动后的uploader对象)，status(http状态码)
将录音发送给web(websocket，js)
1. websocket进行转发
web收到录音播放
1. 收到字符串{sender, receiver, data}
2. 通过Flask中的send_file实现audio src 网络路径 播放语音文件
```

# 智能玩具

## Day1

### 1. 数据采集

-   寻找内容提供商：贝瓦，听(喜马拉雅，学前教育)，中国某知名内容提供厂商
-   mp3和mp4a本质是一样的
-   条形码：只能存储数字

```python
# xiaopapa.py
# 请求不到数据时，需要使用user_agent,x_sign等请求头内容
header = {'user_agent':'xxx'}
res = resquests.get(url, headers=header)
# 通过序列化和反序列化进行flase和true的格式转换
```

```python
# config.py
# 生成随机字符串
from uuid import uuid4
str = uuid4()
```

### 2. 使用MongoDB分析

1.  MongoDB 很快，json存储方便，不使用原生sql，数据存储方便
2.  数据后期方便 - 用户画像(根据用户操作日志)
3.  mongodb一次插入多条数据
    -   优势：一次操作库操作即可
    -   劣势：内容出现问题，数据库和内容不同步(try except finally)
4.  忽略密码
    -   `content_list = mongo.content.find({}, {'password':0})`
5.  特点
    -   使用`find({})`在mongodb中查找得到的是生成器对象
    -   使用find_one({})查找得到的是一个`dict类型数据`

### 3. API接口

```python
# flask提供服务
/content_list				# 获取资源内容
/get_cover/filename			# 获取cover
/get_music/filename			# 获取music
/reg						# 注册成功后返回login页面
/login						# 登录，返回除password外的 user 信息
/auto_login					# index页面请求，返回除password外的 user 信息
/scan_qr					# 用户扫描二维码，接着绑定玩具
```

## day2

### 1. API接口

```python
/scan_qr					# 对toy的uuid进行校验，不合法、未绑定、已绑定
/bind_toy					# 通过app绑定toy，并建立两者的关系
/toy_list					# 获取app绑定的所有toy
```

### 2. websocket

```python
# websocket 连接并保持连接
# websocket的使用流程
1. 导入相关包
import json
from flask import Flask, request
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
from geventwebsocket.websocket import WebSocket # 用于语法提示即：#type:WebSocket
ws = Flask(__name__)
web_socket = {}

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 9528), ws, handler_class=WebSocketHandler)
    http_server.serve_forever()
```

## day3

### 1. API

-   通过 user_id 从 users 表中查找并返回 friend_list中的内容

```python
/friend_list			# 获取朋友列表
```

-   通过 chat_id 获取聊天记录，需要限制聊天记录条数
    -   注意，需要清空该聊天窗口的未读消息

```python
/chat_list				# 获取历史聊天记录
```

-   App发送语音消息
    1.  发送id、接收id、语音文件(.amr 语音文件，需要进行转码)
    2.  转码保存到指定文件夹，删除转码前的 amr 的文件
    3.  chats表中更新聊天记录信息
    4.  在 redis 中存储未读消息条数
    5.  查找 toy 中 app 的 remark，并使用百度ai合成消息提示音

```python
/app_uploader			# app 发送语音消息
```

-   toy发送语音消息
    1.  发送id、接收id、语音文件，注意接收的语音文件名
    2.  保存语音文件到指定文件夹
    3.  chats表中更新聊天记录信息
    4.  在 redis 中存储未读消息条数
    5.  判断 toy 通信对象是 toy 还是 app，找到对应的 remark
    6.  如果是 toy 则使用百度ai合成消息提示音
    7.  不是toy 则直接返回

```python
/toy_uploader 			# toy 发送语音消息
```

-   只有 toy 端需要
    1.  从 toy 中查找 friend_remark 即在 friend_list 中的备注
    2.  使用 BaiduAI合成消息提示音
    3.  查找 聊天记录表，并从redis中获取未读条数
    4.  先反转聊天记录在添加语音提示，并返回

```python
/recv_msg				# toy 接收语音消息
```

## day4

### 1. API

-   使用 BaiduAI 语音识别，并对接图灵机器人

```python
/ai_uploader			# 处理 toy 的语音指令
						# 对接图灵机器人
```

### 2. 功能

```python
BaiduAI ASR 			# 语音识别、语音合成
Redis					# 使用 redis 记录
```

## day5

### 1. API

-   添加好友请求
    1.  判断请求方的身份 toy/app
    2.  构造 请求信息并写入数据库

```python
/add_req				# 添加好友请求
```

-   获取请求信息
    1.  通过 user_id 获取所有绑定玩具 id
    2.  通过 $in (mongdb)，查找所有绑定玩具的添加好友的请求信息

```python
/add_req				# 添加好友请求
```

-   处理请求信息
    1.  拒绝：只要修改status状态信息即可
    2.  接收：
        1.  为当前 req_id 和 toy_id 创建一个 chat_win
        2.  构造被添加的 toy 信息
        3.  更新 toy的 friend_list
        4.  判断 请求方类型 app/toy
        5.  构造 toy 中的 friend_list 信息
        6.  更新 请求方的 friend_list
        7.  更新 chat_win 的 user_list 字段

```python
/ref_req				# 拒绝好友请求
/acc_req				# 接受好友请求
```

### 2. 功能

```python
# 对接图灵机器人
toy 之间的对话，语音提醒
```
