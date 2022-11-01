from pydantic import BaseModel

class EmailConfig(BaseModel):
    email: str
    email_password: str