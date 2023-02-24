import time
import django
import json
import os
import pika
from django.apps import apps
# from products.models import Product
# from django.conf import settings
# settings.configure()
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
# django.setup()
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):

        """Handle the command"""
        self.stdout.write('Connecting Consumer ...')
        params = pika.URLParameters("amqps://vcayylrz:NYidTKThVWAYnMQ1KCx-YhsO4WxlTyfW@dingo.rmq.cloudamqp.com/vcayylrz")
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue="admin")

        def callback(ch, method, properties, body):

            print("Received in admin")

            id = json.loads(body)
            print(id)
            Product = apps.get_model("products", "Product")

            product_obj = Product.objects.get(id=id)
            product_obj.likes += 1
            product_obj.save()
            print("Product likes increased! ", id)
            self.stdout.write(self.style.SUCCESS('Product likes increased!'))

        channel.basic_consume(queue="admin", on_message_callback=callback, auto_ack=True)
        print("Started Consuming")
        channel.start_consuming()
        channel.close()

