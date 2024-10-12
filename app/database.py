from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import FastAPI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME") 

try:
    mongo_client = AsyncIOMotorClient(MONGODB_URL)
    db = mongo_client.get_database(DATABASE_NAME)
    print("MongoDB connected.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Disconnect from MongoDB
async def close_mongo_connection() -> None:
    if mongo_client is not None:
        mongo_client.close()
        print("MongoDB disconnected.")

