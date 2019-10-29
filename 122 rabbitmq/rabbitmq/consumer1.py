import pika

# 建立与rabbitmq的连接
credentials = pika.PlainCredentials("henry", "123")
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.44.142', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue="订单")


def callback(ch, method, properties, body):
    print("消费者接收到了订单：%r" % body.decode("utf8"))


# 有消息来临，立即执行callbak，没有消息则夯住，等待消息，队列名字是订单
channel.basic_consume("订单", on_message_callback=callback, auto_ack=True, )
# 开始消费，接收消息
channel.start_consuming()
