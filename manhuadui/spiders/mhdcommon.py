# -*- coding: utf-8 -*-
import re
import os
import logging
from urllib import parse
import scrapy
from manhuadui.settings import IMAGES_STORE
from manhuadui.crytest import get_secret_url
from manhuadui.items import Manhuadui_img_Item


def get_full_img_urls(img_urls, chapterPath, domain='https://img01.eshanyao.com'):
    full_img_urls = []
    for img_url in img_urls:
        if re.match(r'^https?:\/\/(images.dmzj.com|imgsmall.dmzj.com)', img_url, flags=re.IGNORECASE):
            full_img_urls.append('https://img01.eshanyao.com/showImage.php?url=' + parse.quote(img_url))
            # full_img_urls.append('https://img01.eshanyao.com/showImage.php?url=' + img_url)
        elif re.match(r'^[a-z]\/', img_url, flags=re.IGNORECASE):
            full_img_urls.append(
                'https://img01.eshanyao.com/showImage.php?url=' + parse.quote("https://images.dmzj.com/" + img_url))
                # 'https://img01.eshanyao.com/showImage.php?url=' + "https://images.dmzj.com/" + img_url)
        elif re.match(r'^(http:|https:|ftp:|^)\/\/', img_url, flags=re.IGNORECASE):
            full_img_urls.append(img_url)
        else:
            filename = chapterPath.strip('/') + '/' + img_url.lstrip('/')
            full_img_urls.append(domain + '/' + filename)

    return full_img_urls


class MhdcommonSpider(scrapy.Spider):
    name = 'mhdcommon'
    allowed_domains = ['www.manhuadui.com']
    start_urls = [
        'https://www.manhuadui.com/manhua/yidanfangchuchaojuebishajizhouwei100miyineidenvxingjiuhuibianchengdouMkewangyuwoweiaiguzhangwotainanle/']
    mh_title = ''

    def __init__(self, url=None, *args, **kwargs):
        super(MhdcommonSpider, self).__init__(*args, **kwargs)
        logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                            datefmt="%Y/%d/%m %H:%M:%S")
        # import coloredlogs
        # coloredlogs.install(level='INFO')

        if url is not None:
            self.start_urls = [url]

    def parse(self, response):
        self.mh_title = response.xpath('//h1/text()')[0].extract()
        index = response.xpath("//ul[@id='chapter-list-1']")[0]
        chapter_list = index.xpath("./li")
        for li in chapter_list:
            link = li.xpath('./a/@href').extract()[0]
            title = li.xpath('./a/@title').extract()[0]
            full_url = response.urljoin(link)
            metadata = {"title": title}
            yield scrapy.Request(url=full_url, callback=self.chapter_parse, meta=metadata)

    def chapter_parse(self, response):
        title = response.meta['title']
        ret = re.search(r'chapterImages = "(.*?)"', response.text)
        text = ret.group(1)
        img_urls = get_secret_url(text)

        ret = re.search(r'chapterPath = "(.*?)"', response.text)
        chapterPath = ret.group(1)

        full_img_urls = get_full_img_urls(img_urls, chapterPath)

        for index, img_url in enumerate(full_img_urls):

            image_type = os.path.splitext(img_url)[1]
            path = self.mh_title + '/' + title + '/' + str(index + 1) + image_type
            if not os.path.exists(os.path.join(IMAGES_STORE, path)):
                item = Manhuadui_img_Item()
                item['manga_name'] = self.mh_title
                item['chapter_name'] = title
                item['file_name'] = index + 1
                item['link'] = img_url
                item['image_type'] = image_type
                item['path'] = path
                logging.info(path + '加入下载')
                yield item
            else:
                logging.info(path + '已存在')
