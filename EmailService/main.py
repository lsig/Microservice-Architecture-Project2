from infrastructure.container import Container
from infrastructure.settings import Settings
import threading

settings = Settings("./infrastructure/.env")
container = Container()
container.config.from_pydantic(settings)

receiver = container.receiver_provider()

#payment_receiver = threading.Thread(target=receiver.consume_payment)
#order_receiver = threading.Thread(target=receiver.consume_order)

if __name__ == '__main__':
    #order_receiver.start()
    #payment_receiver.start()
    print("Waiting ...")
    receiver.consume()