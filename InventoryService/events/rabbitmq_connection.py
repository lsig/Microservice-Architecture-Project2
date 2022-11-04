import pika
from retry import retry

from events.rabbitmq_config import RabbitmqConfig

class RabbitmqConnection:
    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __init__(self, rabbit_config: RabbitmqConfig):
        credentials = pika.PlainCredentials(rabbit_config.user, rabbit_config.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_config.host, port=rabbit_config.port, virtual_host='/', credentials=credentials, heartbeat=600))