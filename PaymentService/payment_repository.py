from connections.mongodb_connection import MongoDbConnection

class PaymentRepository:
    def __init__(self, connection: MongoDbConnection):
        self.__collection = connection.collection
    
    async def fetch_payment(self, id: int): 
        document = await self.__collection.find_one({"orderId":id})
        return document
    
    async def post_payment(self, payment: dict):
        document = payment
        result = await self.__collection.insert_one(document)
        return result