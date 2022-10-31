from fastapi import FastAPI
import uvicorn
from infrastructure.container import Container

from infrastructure.settings import Settings
from inventory_endpoints import router
import inventory_endpoints

settings = Settings("./infrastructure/.env")

def start_app():
    container = Container()
    container.config.from_pydantic(settings)
    container.wire(modules=[inventory_endpoints])

    app = FastAPI()
    app.container = container
    app.include_router(router)

    return app



app = start_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app_host, port=8003, reload=True)