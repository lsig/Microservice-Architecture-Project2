from infrastructure.container import Container
from models.buyer_model import BuyerModel
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from buyer_repository import BuyerRepository

router = APIRouter()

@router.get('/buyers/{id}', status_code=200, response_model=BuyerModel)
@inject
async def get_buyer(id: str, buyer_repository: BuyerRepository = Depends(
    Provide[Container.buyer_repository_provider])):
    buyer = await buyer_repository.fetch_buyer(id)
    if buyer:
        return buyer
    raise HTTPException(status_code=404, detail=f"There is no buyer with id: {id}")


@router.post('/buyers', response_model=BuyerModel)
@inject
async def save_buyer(buyer: BuyerModel, 
                        buyer_repository: BuyerRepository = Depends(
                        Provide[Container.buyer_repository_provider])):
    buyer = jsonable_encoder(buyer)
    new_buyer = await buyer_repository.post_buyer(buyer=buyer)
    if new_buyer:
        return JSONResponse(status_code=201, content=buyer["_id"])
    raise HTTPException(400, "Bad request")