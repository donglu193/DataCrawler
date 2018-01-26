from pymongo import MongoClient
import numpy as np

# client = MongoClient('localhost:27017')
# db = client.testDB
#
# list_identity = []
# list_shoes = []
#
#
# for item in db.shoe_identity.find({'desc': {'$ne': 'status entry'}}):
#     list_identity.append(item['uniqueId'])
#
# for item in db.shoes.find():
#     list_shoes.append(item['uniqueId'])
#
# main_list = np.setdiff1d(list_identity,list_shoes)
#
# print main_list


def get_url_list():
    # get DB connection
    client = MongoClient('localhost:27017')
    db = client.testDB

    # return list
    list = []

    for item in db.shoe_identity.find():
        print item['uniqueId']
        #find returns a cursor
        shoe_list = db.shoes.find({"uniqueId": item['uniqueId']}).sort([('_id', -1)]).limit(1)
        if shoe_list.count() > 0:
            shoe = shoe_list[0]
            print shoe['objectID']
            url = 'https://stockx.com/api/products/' + shoe['objectID'] + '/activity?state=480'
            sneaker_obj = {'url': url, 'name': item['name'], 'uniqueId': item['uniqueId']}

            list.append(sneaker_obj)

print get_url_list()