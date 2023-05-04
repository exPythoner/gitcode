# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YangguangItem(scrapy.Item):
    # define the fields for your item here like:
    page = scrapy.Field()
    num = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    publish_date = scrapy.Field()
    content_img = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    status = scrapy.Field()
    content_video = scrapy.Field()
    content_author = scrapy.Field()
    content_from = scrapy.Field()
    author_img = scrapy.Field()
    score_list = scrapy.Field()

