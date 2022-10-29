from http.client import HTTPException
from tokenize import String
from urllib import response
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from models.merchant_model import MerchantModel
from database import fetch_merchant, create_merchant
from infrastructure.container import Container

router = APIRouter()

@router.get('/merchants/{id}', status_code=200, response_model=MerchantModel)
@inject
async def get_message(id: int):
    response = await fetch_merchant(id)
    if response:
        return response
    raise HTTPException(404, f"There is no merchant with this id {id}")


@router.post('/merchants', status_code=201, response_model=MerchantModel)
@inject
async def save_messages(merchant: MerchantModel):
    response = await create_merchant(merchant.dict())
    if response:
        return response
    raise HTTPException(400, "Bad request")