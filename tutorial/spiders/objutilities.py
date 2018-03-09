import datetime
import time


def get_identity_obj(userId, sneakerName, counter):
    sneaker = {}
    sneaker['name'] = sneakerName
    sneaker['uniqueId'] = 'SNKRS-' + str(counter) + '-' + str(time.time())
    sneaker['createdby'] = userId
    sneaker['timecreated'] = str(datetime.datetime.now())

    return sneaker


def get_streetwear_obj(userId, name, counter):
    streetwear = {}
    streetwear['name'] = name
    streetwear['uniqueId'] = 'STRWR-' + str(counter) + '-' + str(time.time())
    streetwear['createdby'] = userId
    streetwear['timecreated'] = str(datetime.datetime.now())

    return streetwear


def get_url_list(category):

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
                url = 'https://stockx.com/api/browse?_tags=' + category + '&' \
                      'productCategory=' + category + '&sort=' + key + \
                      '&order=' + sort +\
                      '&page=' + \
                str(i +1)
                list.append(url)

        return list

