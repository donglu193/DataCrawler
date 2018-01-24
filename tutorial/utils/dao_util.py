from pymongo import MongoClient
import numpy as np

client = MongoClient('localhost:27017')
db = client.testDB

list_identity = []
list_shoes = []


for item in db.shoe_identity.find({'desc': {'$ne': 'status entry'}}):
    list_identity.append(item['uniqueId'])

for item in db.shoes.find():
    list_shoes.append(item['uniqueId'])

main_list = np.setdiff1d(list_identity,list_shoes)

print main_list