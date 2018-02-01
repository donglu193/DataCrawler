import redis
from pymongo import MongoClient


def _init_shoes_identity():
    client = MongoClient('localhost:27017')
    db = client.testDB

    r = redis.StrictRedis(host='localhost', port=6379, db=0, password='donglu123')

    # Clear the cache
    r.delete('shoes_identity')

    # Adding shoe identity to the cache
    for shoe in db.shoe_identity.find():
        flag = r.sadd('shoes_identity', shoe['uniqueId'])
        print '---Adding shoes: ' + shoe['name'] + ' Status: ' + str(flag)


def get_list(name):

    r = redis.StrictRedis(host='localhost', port=6379, db=0, password='donglu123')
    return r.smembers(name)


_init_shoes_identity()
list = get_list('shoes_identity')
print len(list)
