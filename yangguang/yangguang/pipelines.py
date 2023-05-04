# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
collection = client["yangguang"]["yg"]


class YangguangPipeline:
    def process_item(self, item, spider):
        item = self.process_content(item)
        collection.insert_one(dict(item))
        print("\n{0}{1}{0}\n".format("-" * 50, " Starting Pipeline Print... "))
        pprint(item)
        return item

    def process_content(self, item):
        content = [re.sub(r"\r\n", "", i) for i in item["content"]]
        item["content"] = [i.strip() for i in content if len(i) > 0]  # 去除列表中的空字符串
        item["time"] = item["time"].strip()
        item["status"] = item["status"].strip()
        item["content_author"] = item["content_author"].strip()
        item["content_from"] = item["content_from"].replace(" 来自：","")
        return item
