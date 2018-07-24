# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SougounewsItem(scrapy.Item):
    # 分类
    tag=scrapy.Field()
    # 标题
    title=scrapy.Field()
    # 内容简略
    info=scrapy.Field()
    # 发布时间
    time=scrapy.Field()
    # 发布者
    post_user=scrapy.Field()
    # 内容链接
    link=scrapy.Field()

