# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

class CSVPipeline:
    def __init__(self):
        # 创建并打开文件
        self.file = open('data.csv','w',newline='',encoding='utf-8')
        # 获取文件写入对象
        self.writer = csv.writer(self.file)
        # 写入表头
        self.writer.writerow(['brand','tags','price'])
    # 将数据保存到csv文件中
    def process_item(self, item, spider):
        # 写入数据
        self.writer.writerow([item.get('brand'),item.get('tags'),item.get('price')])
    def close_spider(self,spider):
        # 关闭文件
        self.file.close()
