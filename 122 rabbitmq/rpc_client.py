import pika

# 建立连接，服务器地址为localhost，可指定ip地址

credentials = pika.PlainCredentials("henry", "123")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='172.16.44.142', credentials=credentials), )
# 建立会话
channel = connection.channel()
# 声明RPC请求队列
channel.queue_declare(queue='rpc_test',)


# 模拟一个进程，例如切菜师傅，等着洗菜师傅传递数据
def sum(n):
    n += 100
    return n


# 对RPC请求队列中的请求进行处理

def on_request(ch, method, props, body):
    print(body, type(body))
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
channel.basic_consume(queue='rpc_test', on_message_callback=on_request, )
print("等待接收rpc请求")

# 开始消费
channel.start_consuming()
