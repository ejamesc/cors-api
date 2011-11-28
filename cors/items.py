# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CorsItem(Item):
    """Scrapy data structure
    """
    code = Field()
    name = Field()
    desc = Field()
    mc = Field()
    lecture_time_table = Field()
    exam = Field()
    prerequisite = Field()
    preclusion = Field()
    workload = Field()