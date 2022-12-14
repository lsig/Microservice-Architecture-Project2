from dataclasses import Field
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

class BuyerModel(BaseModel):
    id: int = Field(None, alias="_id")  #Better PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    ssn: str
    email: str
    phoneNumber: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "ssn": "4000000000",
                "email": "jdoe@example.com",
                "phoneNumber": "1234567",
            }
        }