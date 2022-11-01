from fastapi import FastAPI
import uvicorn

from order_endpoints import router
from infrastructure.settings import Settings
from infrastructure.container import Container
import order_endpoints


def create_app(container: Container) -> FastAPI:

    app = FastAPI()
    app.container = container
    app.include_router(router)

    return app


settings = Settings("./infrastructure/.env")
container = Container()
container.config.from_pydantic(settings)
container.wire(modules=[order_endpoints])

app = create_app(container)


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
