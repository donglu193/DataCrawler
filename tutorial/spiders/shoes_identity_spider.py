import scrapy
import json
from pymongo import MongoClient
import objutilities


class TestSpider(scrapy.Spider):
    #spider name
    name = "shoes_identity"
    #set default value for counter
    counter = 0
    shoe_list = []

    def start_requests(self):

        start_url = objutilities.get_url_list()

        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        data = json.loads(response.body, 'UTF-8')

        client = MongoClient('localhost:27017')
        db = client.testDB

        for obj in data['Products']:

            #get sneaker name and increment counter
            snkrs_name = obj['urlKey']

            if snkrs_name not in self.shoe_list:
                self.counter += 1
                sneaker_obj = objutilities.get_identity_obj('Admin', snkrs_name, self.counter)
                db.shoe_identity.insert_one(sneaker_obj)
                self.shoe_list.append(snkrs_name)
                print "------Inserted sneaker: " + snkrs_name








