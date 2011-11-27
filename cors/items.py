# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CorsItem(Item):
    # define the fields for your item here like:
    code = Field()
    desc = Field()
    name = Field()
    mc = Field()
    lecture_time_table = Field()
    exam = Field()
    prerequisite = Field()
    preclusion = Field()
    workload = Field()