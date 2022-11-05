from pydantic import BaseModel


class BuyerResponse(BaseModel):
    name: str
    ssn: str
    email: str
    phoneNumber: str
