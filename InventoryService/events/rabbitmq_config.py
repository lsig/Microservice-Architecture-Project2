from pydantic import BaseModel

class RabbitmqConfig(BaseModel):
    host: str
    port: str
    user: str
    password: str