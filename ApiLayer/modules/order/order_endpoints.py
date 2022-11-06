from fastapi import APIRouter, Response
from dependency_injector.wiring import inject
from requests import get, post

from modules.order.models.order_model import OrderModel


router = APIRouter(
    prefix="/orders"
)


ORDER_CONTAINER="order_service:8000"

@router.get(path="/{id}", status_code=200)
@inject
async def get_order(id: int, response: Response):
    order_response = get(f"http://{ORDER_CONTAINER}/orders/{id}")
    response.status_code = order_response.status_code
    return order_response.json()



@router.post(path="", status_code=201)
@inject
async def post_order(order: OrderModel, response: Response):
    order_response = post(f"http://{ORDER_CONTAINER}/orders", data=order.json())
    response.status_code = order_response.status_code
    return order_response.json()
