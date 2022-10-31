import pika
from retry import retry

from connections.rabbit_config import RabbitConfig

class OrderReceiver:
    def __init__(self, rabbit_config: RabbitConfig) -> None:
        self.connection = self.__get_connection(rabbit_config)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=rabbit_config.exhange, exchange_type=rabbit_config.exhange_type)
        result = self.channel.queue_declare(queue='')
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=rabbit_config.exhange, queue=self.queue_name)


    def callback(self, ch, method, properties, body):
        pass

    def consume(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    
    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self, rabbit_config: RabbitConfig):
        credentials = pika.PlainCredentials(rabbit_config.user, rabbit_config.password)
        return pika.BlockingConnection(pika.ConnectionParameters(host='host.docker.internal', port='5672', virtual_host='/', credentials=credentials))