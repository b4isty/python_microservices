import json

import pika

params = pika.URLParameters("amqps://vcayylrz:NYidTKThVWAYnMQ1KCx-YhsO4WxlTyfW@dingo.rmq.cloudamqp.com/vcayylrz")
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange="", routing_key="main", body=json.dumps(body), properties=properties)
