#!/usr/bin/env python
#docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management

import threading
import pika
import sys
import math
import time
import numpy as np
import signal
import json

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

global maior
global menor

global j
j=0


V_SIZE = int(sys.argv[2])
maior= 0
menor=1e9

def signal_handler(sig, frame):
    print('Encerrando...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def callback(ch, method, properties, body):
    global maior
    global menor
    global j
    body = json.loads(body)
    print(" [x] %r:%r" % (method.routing_key, body))
    j+=1
    if(body[0] < menor):
        menor = body[0]
    if(body[1] > maior):
        maior = body[1]
    if(j == int(nMaquinas)):
        print(f"Os maiores e menores valores recebidos foram :\n Maior: {maior}\n Menor: {menor}")
        sys.exit(0)


def func():
    connectionForResponse = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channelForResponse = connectionForResponse.channel()
    channelForResponse.exchange_declare(exchange='resolve_vetor', exchange_type='topic')
    resultResponse = channelForResponse.queue_declare('',exclusive=False)
    queue_name_response = resultResponse.method.queue
    channelForResponse.queue_bind(
    exchange='resolve_vetor', queue=queue_name_response, routing_key="resultado"
    )
    channelForResponse.basic_consume(
    queue=queue_name_response, on_message_callback=callback, auto_ack=True)
    channelForResponse.start_consuming()
    connection.close()



x = threading.Thread(target=func)
x.daemon = True
x.start()
time.sleep(1)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='resolve_vetor', exchange_type='topic')
channelList = list(sys.argv[1].split(','))
nMaquinas = len(channelList)
result = channel.queue_declare('', exclusive=False)
queue_name = result.method.queue
array100 = []
for i in range(V_SIZE):
    array100.append((i-V_SIZE/2)**2)
    array100[i] = math.sqrt(int(array100[i]))
    array100[i] = int(array100[i])

split = np.array_split(array100, nMaquinas)
# print("arr = ", array100)


for k, channels in enumerate(channelList):
    routing_key = channels
    split[k] = list(split[k])
    bA = json.dumps(split[k], default=np_encoder)
    channel.basic_publish(
        exchange='resolve_vetor', routing_key=routing_key, body=bA)
    # print(" [x] Sent %r:%r" % (routing_key, split[k]))
    k+=1

x.join()

