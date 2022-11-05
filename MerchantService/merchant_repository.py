from database.mongodb_connection import MongoDbConnection


class MerchantRepository:
    def __init__(self, connection: MongoDbConnection):
        self.__collection = connection.collection
    
    async def fetch_merchant(self, id: int): 
        document = await self.__collection.find_one({"_id":id}, {"_id": 0})
        return document
    
    async def post_merchant(self, merchant: dict):
        document = merchant
        ### Would normally use pyobject, see merchant model
        document["_id"] = await self.__collection.count_documents({}) + 1
        result = await self.__collection.insert_one(document)
        return result