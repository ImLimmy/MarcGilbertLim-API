from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

class Database:
    def __init__(self, uri:str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client['user_management_db']

db = Database('mongodb://127.0.0.1:27017')