from pydantic import BaseModel


class BuyerModel(BaseModel):
    id: int
    name: str
    ssn: str
    email: str
    phone_number: str