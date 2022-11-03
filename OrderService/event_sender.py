from models.order_event_model import OrderEventModel
from db_connection.rb_connection import RabbitMQConnection

class EventSender:
    def __init__(self, connection: RabbitMQConnection) -> None:
        self.connection = connection.connection
        self.channel = self.initialize_channel()
        
    def initialize_channel(self):
        channel = self.connection.channel()
        channel.exchange_declare(exchange='order_created', exchange_type='fanout')
        return channel

    def send_order_created_event(self, order: OrderEventModel):
        self.channel.basic_publish(exchange='order_created', routing_key='', body=order.json())
