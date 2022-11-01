



from events.i_event_connection import IEventConnection
from events.rabbitmq_config import RabbitmqConfig


class RabbitmqConnection(IEventConnection):
    def __init__(self, rabbitmq_config: RabbitmqConfig) -> None:
        self.config = rabbitmq_config
        super().__init__()