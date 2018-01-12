import scrapy
import json
from pymongo import MongoClient


class TestSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):

        start_url = [
            'https://stockx.com/api/browse?page=1&category=152&sort=most-active&order=DESC&time=1515556092901',
        ]

        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        data = json.loads(response.body, 'UTF-8')
        # filename = 'stockx-file.json'
        # f = open(filename, 'wb')

        # for obj in data['Products']:
        #     f.write(str(obj))
        #     f.write('/n')

        client = MongoClient('localhost:27017')
        db = client.testDB

        for obj in data['Products']:
            db.shoes.insert_one(obj)

