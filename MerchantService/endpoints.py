from infrastructure.container import Container
from models.merchant_model import MerchantModel
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from merchant_repository import MerchantRepository

router = APIRouter()

@router.get('/merchants/{id}', status_code=200)
@inject
async def get_merchant(id: int, merchant_repository: MerchantRepository = Depends(
    Provide[Container.merchant_repository_provider])):
    merchant = await merchant_repository.fetch_merchant(id)
    if merchant:
        return merchant
        
    raise HTTPException(status_code=404, detail=f"There is no merchant with id: {id}")


@router.post('/merchants', response_model=MerchantModel)
@inject
async def save_merchant(merchant: MerchantModel, 
                        merchant_repository: MerchantRepository = Depends(
                        Provide[Container.merchant_repository_provider])):
    merchant = jsonable_encoder(merchant)
    new_merchant = await merchant_repository.post_merchant(merchant=merchant)
    if new_merchant:
        return JSONResponse(status_code=201, content=merchant["_id"])
    raise HTTPException(400, "Bad request")