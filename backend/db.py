from pymongo import MongoClient
import os

class MongoDB:
    def __init__(self, uri=None, db_name=None):
        self.uri = uri or os.getenv('MONGO_URI', 'mongodb://localhost:27017/chessrpg')
        self.db_name = db_name or os.getenv('MONGO_DB', 'chessrpg')
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]

    def get_collection(self, name):
        return self.db[name]

# Example usage:
# db = MongoDB()
# users = db.get_collection('users')
# users.insert_one({'username': 'test'})
