from pydantic import BaseModel

class RabbitConfig(BaseModel):
    user: str
    password: str
    exhange: str
    exhange_type: str