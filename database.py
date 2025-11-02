from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import Config
import ssl

class Database:
    def __init__(self):
        try:
            # Create a new client and connect to the server
            self.client = MongoClient(
                Config.MONGODB_URI, 
                server_api=ServerApi('1'),
                tls=True,
                tlsAllowInvalidCertificates=False
            )
            
            # Send a ping to confirm a successful connection
            self.client.admin.command('ping')
            print("✅ Pinged your deployment. You successfully connected to MongoDB Atlas!")
            
            self.db = self.client.get_database('taskdb')
            
        except Exception as e:
            print(f"❌ MongoDB connection error: {e}")
            raise
    
    def get_collection(self, name):
        return self.db[name]

# Global database instance
db = Database()