from database.mongodb_connection import MongoDbConnection


class BuyerRepository:
    def __init__(self, connection: MongoDbConnection):
        self.__collection = connection.collection
    
    async def fetch_buyer(self, id: str): 
        document = await self.__collection.find_one({"_id":id})
        return document
    
    async def post_buyer(self, buyer: dict):
        document = buyer
        result = await self.__collection.insert_one(document)
        return result