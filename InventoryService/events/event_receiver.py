from json import loads
from requests import patch

from events.rabbitmq_connection import RabbitmqConnection
from inventory_service import InventoryService

class EventReceiver:
    def __init__(self, event_connection: RabbitmqConnection) -> None:
        self.connection = event_connection.connection
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="payment", exchange_type="fanout")
        result = self.channel.queue_declare(queue='')
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange="payment", queue=self.queue_name)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
    


    def callback(self, ch, method, properties, body):
        event_info = loads(body)
        response = patch(f"http://localhost:8003/products/process_payment", json=event_info)

        return response





    def consume(self):
        self.channel.start_consuming()