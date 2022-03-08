#!/usr/bin/env python
#docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management

import pika
import sys
import threading
import time


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='resolve_vetor', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='resolve_vetor', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for {0} To exit press CTRL+C'.format(sys.argv[1]))

def callback(ch, method, properties, body):
    print(f'{method.routing_key} : {list(body)}')
    message = [min(list(body)),max(list(body))]
    routing_key = 'resultado'
    channel.basic_publish(
            exchange='resolve_vetor', routing_key=routing_key, body=bytearray(message))
    # print(" [x] Sent %r:%r" % (routing_key, message))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()