# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class ManhuaduiPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagesPipiline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 从item中获取要下载的图片的url，根据url构造Request()对象，并返回该对象
        image_url = item['link']
        yield Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        # 用来自定义图片的下载路径
        item = request.meta['item']
        path = item['path']

        return path

    def item_completed(self, results, item, info):
        # 图片下载完成后，返回结果result
        # print(results)
        logging.warning("{下载成功" if results[0][0] else "下载失败")
        logging.warning(results[0][1]['path'] + ' ' + results[0][1]['url'] + '}')
        return item
