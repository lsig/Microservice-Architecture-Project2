from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from infrastructure.container import Container
from inventory_service import InventoryService
from typing import List

from models.product_response_model import ProductResponseModel
from models.product_model import ProductModel





router = APIRouter()


@router.get(path="/products/{id}", status_code=200)
@inject
async def get_product(id: int, inventory_service: InventoryService = Depends(Provide[Container.inventory_service_provide])) -> ProductResponseModel:
    return inventory_service.get_product(id)


@router.get(path="/products/all/by_merchant/{id}", status_code=200, include_in_schema=True)
@inject
async def get_all_products_by_merchant_id(id: int, inventory_service: InventoryService = Depends(Provide[Container.inventory_service_provide])) -> List[ProductResponseModel]:
    return inventory_service.get_all_products_by_merchant_id(id)


@router.post(path="/products", status_code=201)
@inject
async def post_product(product: ProductModel, inventory_service: InventoryService = Depends(Provide[Container.inventory_service_provide])) -> int:
    return inventory_service.save_products(product)


@router.patch(path="/products/reserve/{id}", status_code=201, include_in_schema=False)
@inject
async def reserve_product(id: int, inventory_service: InventoryService = Depends(Provide[Container.inventory_service_provide])):
    return inventory_service.reserve_product(id)