from pymongo import MongoClient


def initial_shoe_list():
    client = MongoClient('localhost:27017')
    db = client.testDB

    shoe_list = []

    for shoe in db.shoe_identity.find({'desc': {'$ne': 'status entry'}}):
        shoe_list.append(shoe)

    return shoe_list