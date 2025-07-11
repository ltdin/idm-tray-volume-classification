from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["tray_counting"]
versions_collection = db["model_versions"]
