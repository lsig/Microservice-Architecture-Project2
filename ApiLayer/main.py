from fastapi import FastAPI
import uvicorn

# from infrastructure.settings import Settings
# from infrastructure.container import Container
from modules.order import order_endpoints 
from modules.merchant import merchant_endpoints
from modules.inventory import inventory_endpoints
from modules.buyer import buyer_endpoints 


endpoint_modules=[order_endpoints, merchant_endpoints, inventory_endpoints, buyer_endpoints]

def create_app() -> FastAPI:

    app = FastAPI()
    # app.container = container
    return app


# settings = Settings("./infrastructure/.env")
# container = Container()
# container.config.from_pydantic(settings)
# container.wire(modules=[order_endpoints])

app = create_app()

for module in endpoint_modules:
        app.include_router(module.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
