from database.mongodb_connection import MongoDbConnection


class MerchantRepository:
    def __init__(self, connection: MongoDbConnection):
        self.__collection = connection.collection
    
    async def fetch_merchant(self, id: str): 
        document = await self.__collection.find_one({"_id":id})
        return document
    
    async def post_merchant(self, merchant: dict):
        document = merchant
        result = await self.__collection.insert_one(document)
        return result