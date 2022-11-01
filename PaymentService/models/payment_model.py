from pydantic import BaseModel, Field
from bson.objectid import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class PaymentModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    order_id: int 
    product_id: int
    payment_succsess: bool


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "order_id": 35,
                "product_id": 12,
                "payment_succsess": True
            }
        }
