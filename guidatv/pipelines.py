# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.utils.serialize import ScrapyJSONEncoder

class JsonWriterPipeline:
    guidatv = {
        'schedules': []
    }
    def open_spider(self, spider):
        self.file = open('guidatv.json', 'w')

    def close_spider(self, spider):
        jsonStr = json.dumps(self.guidatv, cls=ScrapyJSONEncoder)
        self.file.write(jsonStr)
        self.file.close()

    def process_item(self, item, spider):
        self.guidatv['schedules'].append(dict(item))
        return item