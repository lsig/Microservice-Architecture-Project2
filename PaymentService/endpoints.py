from infrastructure.container import Container
from models.payment_model import PaymentModel
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from payment_repository import PaymentRepository

router = APIRouter()

@router.get('/payments/{id}', status_code=200, response_model=PaymentModel)
@inject
async def get_payment(id: int, payment_repository: PaymentRepository = Depends(
    Provide[Container.payment_repository_provider])):
    payment = await payment_repository.fetch_payment(id)
    if payment:
        return payment
    raise HTTPException(status_code=404, detail=f"There is no payment with id: {id}")


@router.post('/payments', response_model=PaymentModel)
@inject
async def save_payment(payment: PaymentModel, 
                        payment_repository: PaymentRepository = Depends(
                        Provide[Container.payment_repository_provider])):
    payment = jsonable_encoder(payment)
    new_payment = await payment_repository.post_payment(payment=payment)
    if new_payment:
        print(payment)
        return JSONResponse(status_code=201, content=payment["orderId"])
    raise HTTPException(400, "Bad request")