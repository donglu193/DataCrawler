import scrapy


class StockXSpider(scrapy.Spider):
    name = "stockx"

    print name

    def start_requests(self):

        start_url = [
            'https://stockx.com/sneakers/most-popular',
        ]

        print "after URLs"

        for url in start_url:

            print "Printing the URL: " + url

            yield scrapy.Request(url=url, callback=self.parse)

            print "After the scrapy Request"

    def parse(self, response):
        i = 1

        print "I am in the spider stockx"

        for shoe in response.css('div.browse-grid a.tile'):
            # yield {
            #     'link': shoe.css('::attr(href)').extract_first(),
            #     'name': shoe.css('div.name div::text').extract_first(),
            #     'price_label': shoe.css('div.price-label::text').extract(),
            #     'price': shoe.css('div.price-line div::text')[1].extract()
            # }

            print "Printing the " + str(i) + "shoe"
            print shoe.css('::attr(href)').extract_first()
            print shoe.css('div.name div::text').extract_first()
            print shoe.css('div.price-label::text').extract()
            print shoe.css('div.price-line div::text')[1].extract()
            i = i + 1

    # def parse(self, response):
    #     filename = 'stockx.html'
    #
    #     print filename
    #
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)
