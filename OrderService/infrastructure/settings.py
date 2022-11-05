from pydantic import BaseSettings


class Settings(BaseSettings):
    server_ip: str

    db_host: str
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