# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IldaoTestWithSeleniumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    site = scrapy.Field()
    type = scrapy.Field()
    pay = scrapy.Field()
    etc1 = scrapy.Field()
    etc2 = scrapy.Field()
    etc3 = scrapy.Field()
    numpeople = scrapy.Field()
    phone = scrapy.Field()
    detail = scrapy.Field()
    imageURL = scrapy.Field()
    time = scrapy.Field()
    sponsored = scrapy.Field()
    pass
