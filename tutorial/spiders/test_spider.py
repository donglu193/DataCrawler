import scrapy
import json
import pprint

class TestSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):

        start_url = [
            'https://stockx.com/api/browse?page=1&category=152&sort=most-active&order=DESC&time=1515556092901',
        ]

        for url in start_url:

            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)

        filename = 'stockx-file.json'

        with open(filename, 'wb') as f:
            f.write(str(data))


