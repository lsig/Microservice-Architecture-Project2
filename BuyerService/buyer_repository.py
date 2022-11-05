from database.mongodb_connection import MongoDbConnection


class BuyerRepository:
    def __init__(self, connection: MongoDbConnection):
        self.__collection = connection.collection
    
    async def fetch_buyer(self, id: str): 
        document = await self.__collection.find_one({"_id":id}, {"_id": 0})
        return document
    
    async def post_buyer(self, buyer: dict):
        document = buyer
        document["_id"] = await self.__collection.count_documents({}) + 1
        result = await self.__collection.insert_one(document)
        return result