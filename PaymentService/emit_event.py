import pika
from retry import retry

from models.payment_message_model import PaymentMessageModel


class PaymentSender:
    def __init__(self) -> None:
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="payment", exchange_type="fanout")

    def send_message(self, message: PaymentMessageModel):
        self.channel.basic_publish(exchange='', routing_key='message_queue', body=message)

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        credentials = pika.PlainCredentials('myuser', 'mypassword')
        return pika.BlockingConnection(pika.ConnectionParameters(host='host.docker.internal', port='5672', virtual_host='/', credentials=credentials))
