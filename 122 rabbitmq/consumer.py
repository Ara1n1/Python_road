import pika

credential = pika.PlainCredentials('echo', '123')
connection = pika.BlockingConnection(
    pika.ConnectionParameters('172.16.44.142', virtual_host='vhost1', credentials=credential))

channel = connection.channel()
channel.queue_declare('test', durable=True)


def callback(ch, method, properties, body):
    print("消费者接收到了订单：%r" % body.decode("utf8"))
    # raise Exception('xxx')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume('test', on_message_callback=callback, auto_ack=False)
channel.start_consuming()
