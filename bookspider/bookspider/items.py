# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuanShuWangItem(scrapy.Item):
    # define the fields for your item here like:
    categoryName = scrapy.Field()
    bookName = scrapy.Field()
    bookUrl = scrapy.Field()
    chapterName = scrapy.Field()
    chapterUrl = scrapy.Field()
    chapterContent = scrapy.Field()

    cover = scrapy.Field()
    author = scrapy.Field()
    intro = scrapy.Field()
    number = scrapy.Field()
    pass

class BiQuGeItem(scrapy.Item):
    # define the fields for your item here like:
    bookName = scrapy.Field()
    author = scrapy.Field()
    intro = scrapy.Field()
    cover = scrapy.Field()
    number = scrapy.Field()
    chapterName = scrapy.Field()
    chapterUrl = scrapy.Field()
    chapterContent = scrapy.Field()
    pass
