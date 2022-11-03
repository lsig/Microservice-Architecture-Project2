from infrastructure.container import Container
from infrastructure.settings import Settings

settings = Settings("./infrastructure/.env")
container = Container()
container.config.from_pydantic(settings)

receiver = container.receiver_provider()

if __name__ == '__main__':
    print("Waiting ...")
    receiver.consume()