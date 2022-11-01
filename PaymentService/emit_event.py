from connections.rabbitmq_connection import RabbitMQConnection
from models.payment_model import PaymentModel


class PaymentSender:
    def __init__(self, connection: RabbitMQConnection) -> None:
        self.connection = connection.connection
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="payment", exchange_type="fanout")

    def send_message(self, message: PaymentModel):
        self.channel.basic_publish(exchange='payment', routing_key='', body=message)