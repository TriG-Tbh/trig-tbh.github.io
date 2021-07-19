# DNI

import pymongo
import cogs.settings as settings

client = pymongo.MongoClient(settings.MONGO_URI)

database = client["MainDatabase"]
SETTINGS = database["Settings"]


def find(collection, _id):
    try:
        entry = list(collection.find({"_id": _id}))[0]
    except IndexError:
        return None
    return entry


def add(collection, entry):
    collection.insert(entry)
    SETTINGS = database["settings"]


def update(collection, _id, post):
    collection.update_one({"_id": _id}, {"$set": post}, upsert=True)
    SETTINGS = database["settings"]