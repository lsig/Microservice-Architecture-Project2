from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_database: str
    db_user: str
    db_password: str
    

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'