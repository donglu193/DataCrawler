import scrapy
import json
from pymongo import MongoClient
import dbutilities
import objutilities
import datetime


class TestSpider(scrapy.Spider):
    name = "test"
    shoe_list = dbutilities.initial_shoe_list()
    trans_timestamp = ''
    counter = 0

    def start_requests(self):

        print '------Transaction started------'

        start_url = objutilities.get_url_list()

        #initiate the transaction time
        self.trans_timestamp = str(datetime.datetime.now())
        print '------Transaction time: ' + self.trans_timestamp

        #set the defautl counter for the transaction
        self.counter = 1

        for url in start_url:

            print '------Start to process url: ' + url
            yield scrapy.Request(url=url, callback=self.parse)
            print '------finished process url------'

        print '------Transaction Completeted-------'

    def parse(self, response):

        data = json.loads(response.body, 'UTF-8')

        client = MongoClient('localhost:27017')
        db = client.testDB

        for obj in data['Products']:

            if_exist = False
            snkrs_name = obj['urlKey']


            for shoe in self.shoe_list:
                if shoe['name'] == snkrs_name:
                    if_exist = True
                    if shoe.has_key('transtime') == False or shoe['transtime'] != self.trans_timestamp:

                        #update the transaction time of the current shoe
                        #in case to get duplicate entry for the same update
                        shoe['transtime'] = self.trans_timestamp

                        #update obj body to add trasction time and unique Id
                        obj['uniqueId'] = shoe['uniqueId']
                        obj['transaction_time'] = self.trans_timestamp

                        print '---Inserting shoes into shoes collection: ' + snkrs_name
                        db.shoes.insert_one(obj)
                    break

            #take care of the case when the shoes is not in the cache list
            if if_exist == False:
                #Get identity object
                print '---Pushing the shoes into cache list ' + snkrs_name
                sneaker = objutilities.get_identity_obj('Admin', snkrs_name, self.counter)
                self.counter = self.counter + 1

                #Add to the list in memory
                self.shoe_list.append(sneaker)

                #Add to the db
                print '---Inserting shoes into shoe identity collection ' + snkrs_name
                db.shoe_identity.insert_one(sneaker)

                obj['uniqueId'] = sneaker['uniqueId']
                obj['transaction_time'] = self.trans_timestamp

                print '---Inserting shoes into shoes collection: ' + snkrs_name
                db.shoes.insert_one(obj)



