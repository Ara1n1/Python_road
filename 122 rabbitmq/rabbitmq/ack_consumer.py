import pika
import time

credentials = pika.PlainCredentials("henry", "123")
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.44.142', credentials=credentials))
channel = connection.channel()

# 声明一个队列(创建一个队列)
channel.queue_declare(queue='批量订单')


def callback(ch, method, properties, body):
    print("消费者接受到了任务: %r" % body.decode("utf-8"))
    # 测试报错情况
    # int('asdfasdf')
    # 我告诉rabbitmq服务端，我已经取走了消息
    # 回复方式在这,告诉服务端,我正确消费了消息,你可以标记清除了
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # time.sleep(0.01)


# 关闭no_ack，代表给与服务端ack回复，确认给与回复
channel.basic_consume("批量订单", on_message_callback=callback, auto_ack=False, )
channel.start_consuming()
