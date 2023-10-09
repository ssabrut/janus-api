from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")


class MongoDBClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            # Initialize the MongoDB client here
            cls._instance._client = MongoClient(
                f"mongodb+srv://{DB_USER}:{DB_PASS}@{DB_NAME}/?retryWrites=true&w=majority"
            )
            cls._instance._db = cls._instance._client["angelproject"]
        return cls._instance

    def get_db(self):
        return self._db
