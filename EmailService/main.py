from infrastructure.container import Container
from infrastructure.settings import Settings

settings = Settings("./infrastructure/.env")
container = Container()
container.config.from_pydantic(settings)

order_receiver = container.order_receiver_provider()
payment_receiver = container.payment_receiver_provider()


if __name__ == '__main__':
    order_receiver.consume()
    payment_receiver.consume()