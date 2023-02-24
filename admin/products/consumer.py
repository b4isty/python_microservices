import django
import json
import os
import pika
from .models import Product
# from django.apps import apps

# from django.conf import settings
# settings.configure()
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
# django.setup()


params = pika.URLParameters("amqps://vcayylrz:NYidTKThVWAYnMQ1KCx-YhsO4WxlTyfW@dingo.rmq.cloudamqp.com/vcayylrz")
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue="admin")


def callback(ch, method, properties, body):
    print("Received in admin")
    id = json.loads(body)
    print(id)
    # Product = apps.get_model("products", "Product")
    product = Product.objects.get(id=id)
    product.likes += 1
    product.save()
    print("Product likes increased!")


channel.basic_consume(queue="admin", on_message_callback=callback, auto_ack=True)
print("Started Consuming")
channel.start_consuming()
channel.close()





