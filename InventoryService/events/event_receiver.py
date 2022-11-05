from json import loads
from requests import patch

from events.rabbitmq_connection import RabbitmqConnection
from infrastructure.connection_config import ConnectionConfig

class EventReceiver:
    def __init__(self, event_connection: RabbitmqConnection, connection_config: ConnectionConfig) -> None:
        self.connection = event_connection.connection
        self.server = connection_config
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="payment", exchange_type="fanout")
        result = self.channel.queue_declare(queue='')
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange="payment", queue=self.queue_name)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
    


    def callback(self, ch, method, properties, body):
        print("Processing...")
        event_info = loads(body)
        response = patch(f"http://{self.server.server_ip}:{self.server.this_port}/products/process_payment", json=event_info)
        return response


    def consume(self):
        print("Waiting...")
        self.channel.start_consuming()