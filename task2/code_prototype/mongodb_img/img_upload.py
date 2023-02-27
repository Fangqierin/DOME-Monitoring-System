from pymongo import MongoClient
from config import *

client = MongoClient(
    f"mongodb+srv://{username}:{password}@forumdb.cc36b.mongodb.net/?retryWrites=true&w=majority"
)
db = client["img_receiver"]
collection = db["test"]


image = {"filename": "title", "contents": "content"}
collection.insert_one(image)
