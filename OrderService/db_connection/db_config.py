from pydantic import BaseModel

class DbConfig(BaseModel):
    host: str
    port: str
    database: str
    user: str
    password: str