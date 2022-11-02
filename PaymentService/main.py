import uvicorn
from fastapi import FastAPI
from infrastructure.container import Container
from infrastructure.settings import Settings
import endpoints


def create_app(container: Container) -> FastAPI:
    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    return app
    
settings = Settings("./infrastructure/.env")
container = Container()
container.config.from_pydantic(settings)
#container.wire(modules=[endpoints])

#app = create_app(container)
receiver = container.order_receiver_provider()


if __name__ == '__main__':
    #uvicorn.run('main:app', host='0.0.0.0', port=8004, reload=True)
    print("Waiting for ...")
    receiver.consume()