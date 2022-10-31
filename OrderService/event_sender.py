import pika
from retry import retry
from models.order_model import OrderModel

class EventSender:
    def __init__(self, user, password) -> None:
        self.user = user
        self.password = password
        self.connection = self.__get_connection()
        self.channel = self.initialize_channel()
        

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        return pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port='5672', virtual_host='/', credentials=credentials))


    def initialize_channel(self):
        channel = self.connection.channel()
        channel.exchange_declare(exchange='order_created', exchange_type='fanout')
        
        return channel



    def send_order_created_event(self, order: OrderModel):
        self.channel.basic_publish(exchange='order_created', routing_key='', body=order.json())
