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
