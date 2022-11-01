from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from event_sender import EventSender
from infrastructure.container import Container

from models.order_model import OrderModel
from order_service import OrderService


router = APIRouter()

@router.get('/orders/{id}', status_code=200)
@inject
async def get_order(id: int, order_service: OrderService = Depends(Provide[Container.order_service_provider])):
    return order_service.get_order(id)



@router.post('/orders', status_code=201)
@inject
async def post_order(order: OrderModel, order_service: OrderService = Depends(Provide[Container.order_service_provider])):
    return order_service.post_order(order)