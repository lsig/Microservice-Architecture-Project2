from pydantic import BaseSettings


class Settings(BaseSettings):
    merchant_service_container: str
    buyer_service_container: str
    inventory_service_container: str

    db_host: str
    db_port: str
    db_database: str
    db_user: str
    db_password: str

    rabbitmq_log_host: str
    rabbitmq_log_port: str
    q_user: str
    q_password: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'