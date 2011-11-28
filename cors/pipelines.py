# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.corsdatabase
db['modules'].remove({}) #temporary hack - delete all records

class CorsPipeline(object):
    def process_item(self, item, spider):
    	"""For each item, insert into mongodb as dict
    	"""
    	db['modules'].insert(dict(item))
        return item
