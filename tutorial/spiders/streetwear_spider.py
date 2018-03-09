import scrapy
import json
from pymongo import MongoClient
import dbutilities
import objutilities
import datetime


class TestSpider(scrapy.Spider):
    name = "streetwear"
    streetwear_list = dbutilities.initial_streetwear_list()
    trans_timestamp = ''
    counter = 0

    def start_requests(self):

        print '------Transaction started------'

        start_url = objutilities.get_url_list('streetwear')
        # start_url = [
        #     'https://stockx.com/api/browse?_tags=streetwear&productCategory=streetwear&sort=most-active&order=DESC'
        # ]

        #initiate the transaction time
        self.trans_timestamp = str(datetime.datetime.now())
        print '------Transaction time: ' + self.trans_timestamp

        #set the defautl counter for the transaction
        self.counter = 1

        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        data = json.loads(response.body, 'UTF-8')

        client = MongoClient('localhost:27017')
        db = client.testDB

        for obj in data['Products']:

            if_exist = False
            streetwear_name = obj['urlKey']

            for clothes in self.streetwear_list:
                if clothes['name'] == streetwear_name:
                    if_exist = True
                    if clothes.has_key('transtime') == False or clothes['transtime'] != self.trans_timestamp:

                        #update the transaction time of the current streetwear
                        #in case to get duplicate entry for the same update
                        clothes['transtime'] = self.trans_timestamp

                        #update obj body to add trasction time and unique Id
                        obj['uniqueId'] = clothes['uniqueId']
                        obj['transaction_time'] = self.trans_timestamp

                        print '---Inserting item into streetwear collection: ' + streetwear_name
                        db.streetwear.insert_one(obj)
                    break

            #take care of the case when the streetwear is not in the cache list
            if if_exist == False:
                #Get identity object
                print '---Pushing the item into cache list ' + streetwear_name
                streetwear = objutilities.get_streetwear_obj('Admin', streetwear_name, self.counter)
                self.counter = self.counter + 1

                #Add to the list in memory
                self.streetwear_list.append(streetwear)

                #Add to the db
                print '---Inserting item into streetwear identity collection ' + streetwear_name
                db.streetwear_identity.insert_one(streetwear)

                obj['uniqueId'] = streetwear['uniqueId']
                obj['transaction_time'] = self.trans_timestamp

                print '---Inserting item into streetwear collection: ' + streetwear_name
                db.streetwear.insert_one(obj)



