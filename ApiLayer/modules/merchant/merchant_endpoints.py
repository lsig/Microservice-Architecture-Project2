from fastapi import APIRouter, Response
from dependency_injector.wiring import inject
from requests import get, post

from modules.merchant.models.merchant_model import MerchantModel


router = APIRouter(
    prefix="/merchants"
)


MERCHANT_CONTAINER = "merchant_service:8001"

@router.get(path="/{id}", status_code=200)
@inject
async def get_merchant(id: int, response: Response):
    merchant_response = get(f"http://{MERCHANT_CONTAINER}/merchants/{id}")
    response.status_code = merchant_response.status_code
    return merchant_response.json()



@router.post(path="", status_code=201)
@inject
async def post_merchant(merchant: MerchantModel, response: Response):
    merchant_response = post(f"http://{MERCHANT_CONTAINER}/merchants", data=merchant.json())
    response.status_code = merchant_response.status_code
    return merchant_response.json()