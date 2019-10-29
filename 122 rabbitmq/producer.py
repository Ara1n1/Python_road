import pika

credentials = pika.PlainCredentials('echo', '123')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.44.142', virtual_host='vhost1', credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue='test', durable=True)

channel.basic_publish(exchange='',
                      routing_key='test',
                      body='One order here!',
                      properties=pika.BasicProperties(delivery_mode=2),
                      )
print('下单成功')
connection.close()