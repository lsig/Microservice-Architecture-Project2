from infrastructure.container import Container
from infrastructure.settings import Settings
import threading

settings = Settings("./infrastructure/.env")
container = Container()
container.config.from_pydantic(settings)

order_receiver = container.order_receiver_provider()
payment_receiver = container.payment_receiver_provider()

start_consumer = threading.Thread(target=order_receiver.consume)
start_reciever = threading.Thread(target=payment_receiver.consume)

if __name__ == '__main__':
    start_consumer.start()
    start_reciever.start()
