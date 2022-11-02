from pydantic import BaseModel


class ProductModel(BaseModel):
    id: int
    merchantId: int
    productName: str
    price: float
    quantity: int
    reserved: int