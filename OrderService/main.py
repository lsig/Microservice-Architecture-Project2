from fastapi import FastAPI
import uvicorn

from order_endpoints import router
from infrastructure.settings import Settings
from infrastructure.container import Container
import order_endpoints

def create_app() -> FastAPI:
    settings = Settings("./infrastructure/.env")
    container = Container()
    container.config.from_pydantic(settings)
    container.wire(modules=[order_endpoints])

    app = FastAPI()

    app.container = container
    app.include_router(router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
