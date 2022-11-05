from fastapi import FastAPI
import uvicorn
from infrastructure.container import Container

from infrastructure.settings import Settings
from inventory_endpoints import router
import inventory_endpoints
import threading


def start_app(container: Container) -> FastAPI:

    app = FastAPI()
    app.container = container
    app.include_router(router)

    return app


settings = Settings("./infrastructure/.env")
container = Container()
container.config.from_pydantic(settings)
container.wire(modules=[inventory_endpoints])

app = start_app(container)
event_receiver = container.event_receiver_provide()



if __name__ == "__main__":
    print("inventory service up")
    event_thread = threading.Thread(target=event_receiver.consume)
    event_thread.start()

    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)