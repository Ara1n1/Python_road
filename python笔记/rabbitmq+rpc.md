# 消息队列rabbitmp

## 0. 介绍

### 1.  消息队列

-   **消息队列（Message Queue）是一种应用间的通信方式**，消息发送后可以立即返回，由消息系统来确保消息的可靠传递。
-   消息发布者只管把消息发布到 MQ 中而不用管谁来取，消息使用者只管从 MQ 中取消息而不管是谁发布的。这样发布者和使用者都不用知道对方的存在。

#### 1. 三个角色

1.  队列服务端：rabbitmq
2.  队列生产者
3.  队列消费者

#### 2. 队列产品

1.  RabbitMQ：Erlang编写的消息队列产品，**企业级消息队列软件**，支持消息负载均衡，数据持久化等。
2.  ZeroMQ ：saltstack软件使用此消息，速度最快。
3.  Redis：key-value的系统，也支持队列数据结构，轻量级消息队列
4.  Kafka：由Scala编写，目标是为处理实时数据提供一个统一、高通量、低等待的平台

### 3. 消息队列工作流程

-   生产者，不断的产生消息，并把消息传递给MQ。
-   消费者，一个后台进程，不断的去检测消息队列中是否有消息，有消息就取走，开启新线程去处理业务，如果没有一会再来

### 4. 消息队列作用

1.  程序解耦
    -   允许你独立的扩展或修改两边的处理过程，只要确保它们遵守同样的接口约束。
2.  冗余
    -   消息队列把**数据进行持久化**直到它们已经被完全处理，通过这一方式规避了数据丢失风险。
    -   许多消息队列所采用的"插入-获取-删除"范式中，在把一个消息从队列中删除之前，需要你的处理系统明确的指出该消息已经被处理完毕(**确认机制**)，从而确保你的数据被安全的保存直到你使用完毕。
3.  峰值处理能力
    -   (大白话，就是本来公司业务只需要5台机器，但是临时的**秒杀活动**，5台机器肯定受不了这个压力，我们又不可能将整体服务器架构提升到10台，那在秒杀活动后，机器不就浪费了吗？因此引入消息队列)
    -   在访问量剧增的情况下，应用**仍然需要继续发挥作用**，但是这样的突发流量并不常见。
    -   如果为以能处理这类峰值访问为标准来投入资源随时待命无疑是巨大的浪费。
    -   **使用消息队列能够使关键组件顶住突发的访问压力**，而不会因为突发的超负荷的请求而完全崩溃。
4.  **可恢复性**
    -   系统的一部分组件失效时，不会影响到整个系统。(系统耦合性低)
    -   **消息队列降低了进程间的耦合度**，所以即使一个处理消息的进程挂掉，加入队列中的消息仍然可以在系统恢复后被处理。
5.  顺序保证
    -   在大多使用场景下，**数据处理的顺序都很重要**。
    -   大部分消息队列本来就是排序的，并且能保证数据会按照特定的顺序来处理。（Kafka保证一个Partition内的消息的有序性）
6.  缓冲
    -   采用了**生产者-消费者的设计模式。**
    -   有助于控制和优化数据流经过系统的速度，**解决生产消息和消费消息的处理速度不一致的情况**。
7.  异步通信
    -   很多时候，用户不想也不需要立即处理消息。比如发红包，发短信等流程。
    -   **消息队列提供了异步处理机制**，允许用户把一个消息放入队列，但并不立即处理它。想向队列中放入多少消息就放多少，然后在需要的时候再去处理它们。

### 5. 应用场景

1.  电商订单
    -   检查库存、生成单据、发红包、短信通知等
    -   **订单系统**：用户下单后,订单系统完成持久化处理，将消息写入消息队列，返回用户订单下单成功。
    -   **库存系统**：订阅下单的消息，获取下单消息，进行库操作。 就算库存系统出现故障，消息队列也能保证消息的可靠投递，不会导致消息丢失
2.  秒杀活动
    -   用户的请求，服务器接收到之后，写入消息队列，超过定义的阈值就直接丢弃请求，或者跳转错误页面。
    -   业务系统取出队列中的消息，再做后续处理。

## 1. 安装启动

### 1. 安装

```shell
# 需要安装erlong
yum install -y erlang rabbitmq-server
```

### 2. 启动

```shell
systemctl start rabbitmq-server
systemctl status rabbitmq-server
```

## 2. 配置、管理

### 1. 创建管理员(7)

-   如果登录不进去，很有可能是Linux 的防火墙的缘故。

```python
# 1. 添加用户：henry 密码：123
rabbitmqctl add_user henry 123
# 2. 启动
systemctl start rabbitmq-server
# 3. 给henry设置管理员角色
rabbitmqctl set_user_tags henry administrator
# 4. 设置权限，允许对所有的队列都有权限
# 对何种资源具有配置、写、读的权限通过正则表达式来匹配，具体命令如下：
rabbitmqctl set_permissions [-p <vhostpath>] <user> <conf> <write> <read>
rabbitmqctl set_permissions -p '/' henry '.*' '.*' '.*'
rabbitmqctl set_permissions -p 'vhost1' echo '.*' '.*' '.*'
# 5. 添加web管理页面
rabbitmq-plugins enable rabbitmq_management
# 6. 重启
systemctl restart rabbitmq-server
# 7. 访问
http://172.16.44.142:15672/
# 登录
```

### 2. 单生产者-消费者

-   producer.py

```python
import pika
# 创建凭证，使用rabbitmq用户密码登录
credentials = pika.PlainCredentials("henry","123")
# 新建连接，这里localhost可以更换为服务器ip
connection = pika.BlockingConnection(pimka.ConnectionParameters('172.16.44.142',credentials=credentials))
# 创建频道
channel = connection.channel()
# 声明一个队列，用于接收消息，队列名字叫 订单
channel.queue_declare(queue='订单')
# 注意在rabbitmq中，消息想要发送给队列，必须经过交换(exchange)，初学可以使用空字符串交换(exchange='')，它允许我们精确的指定发送给哪个队列(routing_key=''),参数body值发>送的数据
channel.basic_publish(exchange='',
                      routing_key='订单',
                      body='下了一单')
print("下单成功")
# 程序退出前，确保刷新网络缓冲以及消息发送给rabbitmq，需要关闭本次连接
connection.close()
```

-   环境准备

```shell
pip3 install pika
python3 producer.py
```

-   consumer.py

```python
import pika

# 建立与rabbitmq的连接
credentials = pika.PlainCredentials("henry", "123")
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.44.142', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue="订单")

def callback(ch, method, properties, body):
    print("消费者接收到了订单：%r" % body.decode("utf8"))

# 有消息来临，立即执行callbak，没有消息则夯住，等待消息，队列名字是订单
channel.basic_consume("订单", on_message_callback=callback, auto_ack=True)
# 开始消费，接收消息
channel.start_consuming()
```

```python
python3 consumer.py
```

### 3. 单生产者-多消费者

-   开启多个消费者，默认是轮询机制

### 4. 确认机制

-   消息队列确认机制**保证消息被正确处理**
-   消息队列可以是中文，一般遵循开发文档规范
-   producer.py

```python
import pika
# 创建凭证，使用rabbitmq用户密码登录
credentials = pika.PlainCredentials("henry", "123")
# 新建连接，这里localhost可以更换为服务器ip
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.44.142', credentials=credentials))
# 创建频道
channel = connection.channel()
# 声明一个队列，用于接收消息，队列名字叫 订单
channel.queue_declare(queue='批量订单')
# 注意在rabbitmq中，消息想要发送给队列，必须经过交换(exchange)，初学可以使用空字符串交换(exchange='')，它允许我们精确的指定发送给哪个队列(routing_key=''),参数body值发>送的数据
for i in range(1, 1001):
    channel.basic_publish(exchange='',
                          routing_key='批量订单',
                          body=f'第{i}单')
    if i % 100 == 0:
        print(f'第{i}单下单完毕')
# 程序退出前，确保刷新网络缓冲以及消息发送给rabbitmq，需要关闭本次连接
connection.close()
```

-   ack_consumer.py

```python
import pika,time
credentials = pika.PlainCredentials("henry","123")
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.44.142',credentials=credentials))
channel = connection.channel()

# 声明一个队列(创建一个队列)
channel.queue_declare(queue='批量订单')

def callback(ch, method, properties, body):
	print("消费者接受到了任务: %r" % body.decode("utf-8"))
	# 测试报错情况
	int('asdfasdf')
	# 我告诉rabbitmq服务端，我已经取走了消息
	# 回复方式在这,告诉服务端,我正确消费了消息,你可以标记清除了
	ch.basic_ack(delivery_tag=method.delivery_tag)
	time.sleep(0.01)
		
# auto_ack：默认为True，代表给与服务端ack回复，确认给与回复
channel.basic_consume("批量订单", on_message_callback=callback, auto_ack=False)
channel.start_consuming()
```

## 3. 消息和队列持久化

-   消息和对列是存在内存中的，需要进行持久化操作
-   durable_producer.py

```python
import pika
# 创建凭证，使用rabbitmq用户密码登录
credentials = pika.PlainCredentials("henry", "123")
# 新建连接，这里localhost可以更换为服务器ip
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.44.142', credentials=credentials))
# 创建频道
channel = connection.channel()
# 声明一个队列，用于接收消息，队列名字叫 订单
channel.queue_declare(queue='批量订单', durable=True)
# 注意在rabbitmq中，消息想要发送给队列，必须经过交换(exchange)，初学可以使用空字符串交换(exchange='')，它允许我们精确的指定发送给哪个队列(routing_key=''),参数body值发>送的数据
for i in range(1, 1001):
    channel.basic_publish(exchange='',
                          routing_key='批量订单',
                          body=f'第{i}单',
                          # 代表消息是持久的  2
                          properties=pika.BasicProperties(
                              delivery_mode=2,)
                          )
    if i % 100 == 0:
        print(f'第{i}单下单完毕')
# 程序退出前，确保刷新网络缓冲以及消息发送给rabbitmq，需要关闭本次连接
connection.close()
```

-   durable_consumer.py

```python
import pika
credentials = pika.PlainCredentials("henry", "123")
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.44.142', credentials=credentials))
channel = connection.channel()
# 声明一个队列(创建一个队列)
channel.queue_declare(queue='批量订单', durable=True)

def callback(ch, method, properties, body):
    print("消费者接受到了任务: %r" % body.decode("utf-8"))
    # 我告诉rabbitmq服务端，我已经取走了消息
    # 回复方式在这,告诉服务端,我正确消费了消息,你可以标记清除了
    ch.basic_ack(delivery_tag=method.delivery_tag)

# 关闭no_ack，代表给与服务端ack回复，确认给与回复
channel.basic_consume("批量订单", on_message_callback=callback, auto_ack=False, )
channel.start_consuming()
```

## 4. RPC

-   将一个函数运行在远程计算机上并且等待获取那里的结果，**这个称作远程过程调用RPC**(Remote Procedure Call)。
-   RPC是一个计算机通信协议
-   一种远程调用函数的接口
-   多台服务器之间相互调用
-   socket编程就是RPC通信

### 1. 简介

-   **rpc封装了数据的序列化，反序列化，以及传输协议**
-   由于服务在不同的机器上，远程调用必经网络通信，调用服务必须写一坨网络通信代码，很容易出错且很复杂，因此就出现了RPC框架。

| 公司     | RPC框架 |        |
| -------- | ------- | ------ |
| 阿里巴巴 | Dubbo   | java   |
| 新浪     | Motan   | java   |
| 谷歌     | gRPC    | 多语言 |
| Apache   | thrift  | 多语言 |

### 2. RPC工作流程

-   利用RabbitMQ构建一个RPC系统，包含了客户端和RPC服务器，依旧使用**pika模块**

#### 1. Callback queue

-   一个**客户端向服务器发送请求**，服务器端处理请求后，将其处理结果保存在一个**存储体中**。而客户端为了获得处理结果，那么客户在向服务器发送请求时，同时发送一个回调队列地址`reply_to`。

#### 2. Correlation id

1.  一个客户端可能会**发送多个请求给服务器**，当服务器处理完后，客户端无法辨别在回调队列中的响应具体和那个请求时对应的。为了处理这种情况，客户端在发送每个请求时，同时会附带一个独有`correlation_id`属性，这样客户端在回调队列中据`correlation_id`字段的值就可以分辨此响应属于哪个请求。
2.  **客户端发送请求**：某个应用将请求信息交给客户端，然后客户端发送RPC请求，在发送RPC请求到RPC请求队列时，**客户端至少发送带有reply_to以及correlation_id两个属性的信息**
3.  **服务器端工作流**： 等待接受客户端发来RPC请求，当请求出现的时候，服务器从RPC请求队列中取出请求，然后处理后，将响应发送到reply_to指定的回调队列中
4.  **客户端接受处理结果**： 客户端等待回调队列中出现响应，当响应出现时，它会根据响应中correlation_id字段的值，将其返回给对应的应用

#### 3. 过程

1.  启动rpc客户端，等待接收数据到来，来了之后就进行处理，再将结果丢进队列
2.  启动rpc服务端，发起请求

### 3. 使用

#### 1. rpc_server.py

```python
import pika, uuid
class FibonacciRpcClient(object):
    def __init__(self):
        # 客户端启动时，创建回调队列，会开启会话用于发送RPC请求以及接受响应
        # 建立连接，指定服务器的ip地址
        credentials = pika.PlainCredentials("henry", "123")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.44.142', credentials=credentials))
        # 建立一个会话，每个channel代表一个会话任务
        self.channel = self.connection.channel()

        # 声明回调队列，再次声明的原因是，服务器和客户端可能先后开启，该声明是幂等的，多次声明，但只生效一次
        #exclusive=True 参数是指只对首次声明它的连接可见
        #exclusive=True 会在连接断开的时候，自动删除
		result = self.channel.queue_declare(queue='rpc_test')
        # 将队列指定为当前客户端的回调队列
        self.callback_queue = result.method.queue
        # 客户端订阅回调队列，当回调队列中有响应时，调用`on_response`方法对响应进行处理;
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)


    # 对回调队列中的响应进行处理的函数
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    # 发出RPC请求
    # 例如这里服务端就是一个切菜师傅，菜切好了，需要传递给洗菜师傅，这个过程是发送rpc请求
    def call(self, n):
        # 初始化 response
        self.response = None
        # 生成correlation_id 关联标识，通过python的uuid库，生成全局唯一标识ID，保证时间空间唯一性
        self.corr_id = str(uuid.uuid4())
        # 发送RPC请求内容到RPC请求队列`s14rpc`，同时发送的还有`reply_to`和`correlation_id`
        self.channel.basic_publish(exchange='',
                                   routing_key='test',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

# 建立客户端
fibonacci_rpc = FibonacciRpcClient()

# 发送RPC请求，丢进rpc队列，等待客户端处理完毕，给与响应
print("发送了请求sum(99)")
response = fibonacci_rpc.call(99)

print("得到远程结果响应%r" % response)
```

#### 2. rpc_client.py

```python
import pika
# 建立连接，服务器地址为localhost，可指定ip地址

credentials = pika.PlainCredentials("henry", "123")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='172.16.44.142', credentials=credentials))
# 建立会话
channel = connection.channel()
# 声明RPC请求队列
channel.queue_declare(queue='rpc_test')
# 模拟一个进程，例如切菜师傅，等着洗菜师傅传递数据
def sum(n):
    n+=100
    return n
# 对RPC请求队列中的请求进行处理

def on_request(ch, method, props, body):
    print(body,type(body))
    n = int(body)
    print(" 正在处理sum(%s)" % n)
    # 调用数据处理方法
    response = sum(n)
    # 将处理结果(响应)发送到回调队列
    ch.basic_publish(exchange='',
                     # reply_to代表回复目标
                     routing_key=props.reply_to,
                     # correlation_id（关联标识）：用来将RPC的响应和请求关联起来。
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

# 负载均衡，同一时刻发送给该服务器的请求不超过一个
channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='test')
print("等待接收rpc请求")

#开始消费
channel.start_consuming()
```

# RPC

## 1. 环境准备

```shell
pip install grpcio -i https://pypi.douban.com/simple
pip install grpcio-tools googleapis-common-protos -i https://pypi.douban.com/simple
```

-   gRPC由两个部分构成，grpcio 和 gRPC 工具， 后者是编译 protocol buffer 以及提供生成代码的插件。

```shell
python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ ./*.proto
```

## 2. 使用

### 1. 编写protocol buffer

-   使用 gRPC 首先需要做的是设计 protocol buffer。新建一个 `msg.proto`文件。

```python
syntax = "proto3";

service MsgService {
  rpc GetMsg (MsgRequest) returns (MsgResponse){}
}

message MsgRequest {
    string name = 1;
}

message MsgResponse {
    string msg = 1;
}
```

-   以上面的这个消息服务为例，首先是规定语法，这里使用的是 `proto3` 的语法。接着使用 `service` 关键字定义服务，gRPC 提供4种 RPC 类型的服务，这里定义的是第一种单一请求单一回应，类似普通的函数调用，其他的使用到了 `stream` 关键字，将其放在括号里，代表这个数据是流数据。这个以后再来研究，本次先设计一个简单的RPC。
-   之后定义两个 `message`，一个是请求的结构，一个是回应的结果。 这里表示这个数据结构是字符串，protocol buffer 还可以定义为 int32，int64，double，float 等等。这里赋予的初值可以随便填写，实际使用中，会被赋予新的值。

### 2. 生成接口代码

-   因为之前安装好了一些辅助插件，使用这里直接可以生成。

```bash
python -m grpc_tools.protoc -I . --pythoout=. --grpc_python_out=. msg.proto
```

-   这里会生成两个文件，`msg_pb2.py` 和 `msg_pb2_grpc.py`。这两个文件是为后续的服务端和客户端所用。前者是定义了一些变量，例如 `_MSGREQUEST` 中就包含了请求函数的名字，可接受的变量，实际上还是 `msg.proto` 里定义的东西。

### 3. 创建服务端

-   首先需要导入 RPC 必备的包，以及刚才生成的两个文件。

```python
import grpc
import msg_pb2
import msg_pb2_grpc
```

-   因为 RPC 应该长时间运行，考虑到性能，还需要用到并发的库。

```python
from concurrent import futures
import time

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
```

-   在 Server 中，主要是实现服务，按照 `msg.proto` 定义的，这里需要写一个服务类 `MsgServicer`，这个类需要实现之前定义的 `GetMsg`。 

```python
class MsgServicer(msg_pb2_grpc.MsgServiceServicer):

    def GetMsg(self, request, context):
        print("Received name: %s" % request.name)
        return msg_pb2.MsgResponse(msg='Hello, %s!' % request.name)
```

-   GetMsg 接收到的请求是在 `request` 中，`msg.proto` 中定义的 `name` 就是 `request.name`，接着在 GetMsg 中设计 `msg.proto` 中定义的 `MsgResponse`。
-   之后实现启动服务的部分即可。

```python
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    msg_pb2_grpc.add_MsgServiceServicer_to_server(MsgServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
```

-   通过并发库，将服务端放到多进程里运行。
-   完整 `msg_server.py` 代码如下

```python
import grpc
import msg_pb2
import msg_pb2_grpc

from concurrent import futures
import time

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class MsgServicer(msg_pb2_grpc.MsgServiceServicer):

    def GetMsg(self, request, context):
        print("Received name: %s" % request.name)
        return msg_pb2.MsgResponse(msg='Hello, %s!' % request.name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    msg_pb2_grpc.add_MsgServiceServicer_to_server(MsgServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
```

### 4. 创建客户端

客户端相对简单一些，这里我写了一个简单的客户端。

```python
import grpc

import msg_pb2
import msg_pb2_grpc

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = msg_pb2_grpc.MsgServiceStub(channel)
        response = stub.GetMsg(msg_pb2.MsgRequest(name='world'))
    print("Client received: " + response.msg)


if __name__ == '__main__':
    run()
```

-   使用 `grpc.insecure_channel('localhost:50051')` 进行连接 服务端， 接着在这个 `channel` 上创建 `stub`， 在 `msg_pb2_grpc` 里可以找到 `MsgServiceStub` 这个类相关信息。这个 `stub` 可以调用远程的 `GetMsg` 函数。 `MsgRequest` 中的 `name` 即 `msg.proto` 中定义的数据。在回应里可以得到 `msg.proto` 中定义的 `msg`。

### 5. 运行

-   首先运行 `python msg_server.py` 启动服务端，接着运行 `python msg_client.py` 机会看到客户端接收到了服务端传来的消息。以上就是一个简单的 RPC 的使用。









