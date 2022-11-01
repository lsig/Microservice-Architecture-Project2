import motor.motor_asyncio

from connections.db_config import DbConfig

class MongoDbConnection:
    def __init__(self, db_config: DbConfig):
        client = motor.motor_asyncio.AsyncIOMotorClient(
                host=db_config.host,
                port=db_config.port,
                username=db_config.user,
                password=db_config.password
            )
        merchant_database = client.merchant_list
        self.collection = merchant_database.merchants