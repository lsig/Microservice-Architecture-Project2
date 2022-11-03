import pika
from retry import retry

from db_connection.rb_config import RabbitConfig


class RabbitMQConnection:
    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __init__(self, rabbit_config: RabbitConfig):
        credentials = pika.PlainCredentials(rabbit_config.user, rabbit_config.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_config.host, port=rabbit_config.port, virtual_host='/', credentials=credentials, heartbeat=600))