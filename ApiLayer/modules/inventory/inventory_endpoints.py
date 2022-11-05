from fastapi import APIRouter
from dependency_injector.wiring import inject
from requests import get, post

from modules.inventory.models.product_model import ProductModel


router = APIRouter(
    prefix="/products"
)


INVENTORY_CONTAINER = "inventory_service:8003"

@router.get(path="/{id}", status_code=200)
@inject
async def get_product(id: int):
    response = get(f"http://{INVENTORY_CONTAINER}/products/{id}")
    return response.json()



@router.post(path="", status_code=201)
@inject
async def post_product(product: ProductModel):
    response = post(f"http://{INVENTORY_CONTAINER}/products", data=product.json())
    return response.json()