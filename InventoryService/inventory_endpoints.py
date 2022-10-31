from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from infrastructure.container import Container
from inventory_service import InventoryService

from models.product_response_model import ProductResponseModel
from models.product_model import ProductModel





router = APIRouter()


@router.get(path="/products/{id}", status_code=200)
@inject
async def get_product(id: int, inventory_service: InventoryService = Depends(Provide[Container.inventory_service_provide])) -> ProductResponseModel:
    return inventory_service.get_product(id)


@router.post(path="/products", status_code=201)
@inject
async def post_product(product: ProductModel, inventory_service: InventoryService = Depends(Provide[Container.inventory_service_provide])) -> int:
    return inventory_service.save_products(product)