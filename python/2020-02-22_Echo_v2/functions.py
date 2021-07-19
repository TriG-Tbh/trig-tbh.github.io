import pymongo
from pymongo import MongoClient

import settings

import discord
import random
import datetime

cluster = MongoClient(settings.MONGO_URI)

db = cluster["discord"]

def is_valid_collection(collection):
    if collection in db.collection_names():
        return True
    return False

def search_collection(collection, id):
    if is_valid_collection(collection):
        c = db[collection]
        if c.find_one({"_id": id}) is None:
            return None
        return c.find_one({"_id": id})
    return None

def add_to_collection(collection, post):
    if is_valid_collection(collection):
        c = db[collection]
        c.insert_one(post)
    raise ValueError("collection \"{}\" does not exist".format(collection))

def update(collection, id, modifier):
    if is_valid_collection(collection):
        c = db[collection]
        if c.find_one({"_id": id}) is None:
            raise ValueError("invalid ID")
        try:
            c.update_one({"_id": id}, modifier)
        except pymongo.errors.WriteError:
            raise ValueError("invalid modifier dictionary passed: {}".format(modifier))
    raise ValueError("invalid ID")

def is_sanitized(message):
    if "@everyone" in message or "@here" in message:
        return False
    if "<@" in message:
        return False
    return True

def embed(title, color=None):
    if color is None:
        color = random.randint(0, 0xffffff)
    botembed = discord.Embed(title=title, color=color)
    timestamp = datetime.datetime.utcnow()

    botembed.timestamp = timestamp
    return botembed

