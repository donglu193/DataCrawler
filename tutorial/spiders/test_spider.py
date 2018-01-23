import scrapy
import json
from pymongo import MongoClient
import datetime
import time


class TestSpider(scrapy.Spider):
    name = "test"
    shoe_list = []

    def start_requests(self):

        start_url = self.get_url_list()

        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        data = json.loads(response.body, 'UTF-8')

        ### Saving data to file
        # filename = 'stockx-file.json'
        # f = open(filename, 'wb')

        # for obj in data['Products']:
        #     f.write(str(obj))
        #     f.write('/n')

        client = MongoClient('localhost:27017')
        db = client.testDB
        ### Saving data to file
        # for obj in data['Products']:
        #     db.shoes.insert_one(obj)

        for obj in data['Products']:

            snkrs_name = obj['urlKey']
            sneaker = self.get_identity_obj('Admin', snkrs_name)

            if snkrs_name not in self.shoe_list:
                db.shoe_identity.insert_one(sneaker)
                self.shoe_list.append(snkrs_name)

    def get_identity_obj(self, userId, sneakerName):
        sneaker = {}
        sneaker['name'] = sneakerName
        sneaker['uniqueId'] = 'SNKRS-' + str(time.time())
        sneaker['createdby'] = userId
        sneaker['timecreated'] = str(datetime.datetime.now())

        return sneaker

    def get_url_list(self):

        list = []

        search_keyword = [
            'featured',
            'most-active',
            'recent_asks',
            'recent_bids',
            'average_deadstock_price',
            'deadstock_sold',
            'volatility',
            'price_premium',
            'last_sale',
            'lowest_ask',
            'highest_bid'
        ]
        for key in search_keyword:
            for i in range(25):
                sort = 'DESC'

                if key == 'lowest_ask':
                    sort = 'ASC'
                url = 'https://stockx.com/api/browse?_tags=sneakers&' \
                      'productCategory=sneakers&sort=' + key + \
                      '&order=' + sort +\
                      '&page=' + \
                str(i +1)
                list.append(url)

        return list

