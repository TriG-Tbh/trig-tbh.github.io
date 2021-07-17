import pymongo
from pymongo import MongoClient

cluster = MongoClient(
    "[REDACTED]")

database = cluster["discord"]
#print(database.collection_names())

testcollection = database["poc"]

#print(type(testcollection))

results = testcollection.update_one({"_id": 0}, {"$fdsgdsafset": {"value": "hi"}})
"""print(len(list(results)))
for result in results:
    print(result)"""