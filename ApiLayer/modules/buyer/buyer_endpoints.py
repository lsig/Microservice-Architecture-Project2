from fastapi import APIRouter, Response
from dependency_injector.wiring import inject
from requests import get, post

from modules.buyer.models.buyer_model import BuyerModel


router = APIRouter(
    prefix="/buyers"
)


BUYER_CONTAINER = "buyer_service:8002"

@router.get(path="/{id}", status_code=200)
@inject
async def get_buyer(id: int, response: Response):
    buyer_response = get(f"http://{BUYER_CONTAINER}/buyers/{id}")
    response.status_code = buyer_response.status_code
    return buyer_response.json()



@router.post(path="", status_code=201)
@inject
async def post_buyer(buyer: BuyerModel, response: Response):
    buyer_response = post(f"http://{BUYER_CONTAINER}/buyers", data=buyer.json())
    response.status_code = buyer_response.status_code
    return buyer_response.json()
