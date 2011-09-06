import pymongo
from pymongo import Connection


connection = Connection()
db = connection.test_database
collection = db.test_collection

test=db.test
test.insert({'foo':1,'bar':2})
test.insert({'foo':3,'bar':43232})
test.insert({'foo':3,'baz':43232})

db.collection_names()

test.find_one()

test.find_one({"foo": 3})

for rec in test.find({"foo": 3}):
    rec