from models.merchant_model import MerchantModel
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

merchant_database = client.merchant_list
collection = merchant_database.merchants

async def fetch_merchant(id: int): 
    document = await collection.find_one({"id":id})
    return document

async def create_merchant(merchant: MerchantModel):
    document = merchant
    result = await collection.insert_one(document)
    return result