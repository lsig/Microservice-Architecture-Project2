import uvicorn
from fastapi import FastAPI
from infrastructure.container import Container
from infrastructure.settings import Settings
import endpoints


def create_app() -> FastAPI:
    settings = Settings("./infrastructure/.env")
    container = Container()
    container.config.from_pydantic(settings)
    container.wire(modules=[endpoints])

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)

    return app


app = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)