from pydantic import BaseModel

class DbConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str