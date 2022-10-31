import pika
from retry import retry
from connections.rabbit_config import RabbitConfig
from fastapi import Depends
from dependency_injector.wiring import Provide, inject
from infrastructure.container import Container
from models.payment_model import PaymentMessageModel


class PaymentSender:
    @inject
    def __init__(self, rabbit_config: RabbitConfig = Depends(Provide[Container.rb_config])) -> None:
        self.connection = self.__get_connection(rabbit_config)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="payment", exchange_type="fanout")

    def send_message(self, message: PaymentMessageModel):
        self.channel.basic_publish(exchange='payment', routing_key='', body=message)

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self, rabbit_config):
        credentials = pika.PlainCredentials(rabbit_config.user, rabbit_config.password)
        return pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_config.host, port=rabbit_config.port, virtual_host='/', credentials=credentials))
