from pydantic import BaseModel

class RabbitConfig(BaseModel):
    host: str
    port: str
    user: str
    password: str