from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from infrastructure.container import Container

from models.order_model import OrderModel
from order_service import OrderService


router = APIRouter()

order_service: OrderService = Depends(Provide[Container.order_service_provider])

@router.get('/Order', status_code=200)
async def get_order():
    return "message recieved"


@router.post('/orders', status_code=201)
@inject
async def post_order(order: OrderModel):
    return order_service.post_order(order)