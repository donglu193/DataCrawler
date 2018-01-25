import scrapy
import json
from pymongo import MongoClient
import dbutilities
import datetime


class TestSpider(scrapy.Spider):
    #spider name
    name = "shoes_price"
    shoe_list = dbutilities.initial_shoe_list()

    transaction_time = ''

    def start_requests(self):

        start_url = self.get_url_list()

        # temp_obj = {'url': 'https://stockx.com/api/products/bfb239fe-de89-4bb9-b436-94fa2f5b25fd/activity?state=480',
        #             'name': 'test',
        #             'uniqueId': 'testId'}
        # start_url = [temp_obj]

        self.transaction_time = str(datetime.datetime.now())

        for obj in start_url:
            request = scrapy.Request(url=obj['url'], callback=self.parse)
            request.meta['meta'] = obj
            yield  request

    def parse(self, response):

        data = json.loads(response.body, 'UTF-8')

        if len(data) > 0:
            client = MongoClient('localhost:27017')
            db = client.testDB

            meta = response.meta['meta']
            status = {'url': response.url, 'uniqueId': meta['uniqueId'],
                      'name': meta['name'], 'trans_time': self.transaction_time,
                      'price_list': data}

            db.shoes_price.insert(status)
            print 'Inserted price'
        else:
            print 'empty response'

    def get_url_list(self):
        # get DB connection
        client = MongoClient('localhost:27017')
        db = client.testDB

        # return list
        list = []

        for item in db.shoe_identity.find():
            print item['uniqueId']
            # find returns a cursor
            shoe_list = db.shoes.find({"uniqueId": item['uniqueId']}).sort([('_id', -1)]).limit(1)
            if shoe_list.count() > 0:
                shoe = shoe_list[0]
                print shoe['objectID']
                url = 'https://stockx.com/api/products/' + shoe['objectID'] + '/activity?state=480'
                sneaker_obj = {'url': url, 'name': item['name'], 'uniqueId': item['uniqueId']}

                list.append(sneaker_obj)

        return list

