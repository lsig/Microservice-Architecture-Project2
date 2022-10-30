import motor.motor_asyncio

from database.db_config import DbConfig
from database.db_connection import DbConnection

class MongoDbConnection(DbConnection):
    def __init__(self, db_config: DbConfig):
        client = motor.motor_asyncio.AsyncIOMotorClient(
                host=db_config.host,
                port=db_config.port,
                username=db_config.user,
                password=db_config.password
            )
        print(client)
        buyer_database = client.buyer_list
        self.collection = buyer_database.buyers