# -*- coding: utf-8 -*-
import scrapy
from SougouNews.items import SougounewsItem
import selenium
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
from datetime import datetime


class NewsSpiderSpider(scrapy.Spider):
    name = 'news_spider'
    start_urls = ['http://weixin.sogou.com/']
    def parse(self, response):
        
        # 翻页逻辑
        driver = webdriver.PhantomJS()
        # driver = webdriver.Chrome()
        driver.get("http://weixin.sogou.com/")
        driver.implicitly_wait(3)

        time.sleep(4)
        look_more = ".//div[@class='jzgd']/a"
        # 翻两页
        for n in range(2):
            driver.find_element_by_xpath(look_more).click()
            self.logger.debug("click number")
            time.sleep(2)
        page_source=driver.page_source 
        res=HtmlResponse("http://weixin.sogou.com",body=page_source,encoding='utf-8')



        datas=[]
        news_box=res.css('ul.news-list')
        for item in news_box.css('li'):
            date=item.css('div.txt-box div.s-p span::attr(t)').extract_first()
            if self.filter_time(date)>=1:
                self.logger.debug("time is filtered !")
                continue

            it=SougounewsItem()
            it['title']=item.css('div.txt-box h3 a::text').extract_first()
            it['info']=item.css('div.txt-box p.txt-info::text').extract_first()
            it['time']=date
            it['post_user']=item.css('div.txt-box div.s-p a::text').extract_first()
            it['link']=item.css('div.txt-box h3 a::attr(href)').extract_first()
            datas.append(it)
            yield it
        return datas

    def filter_time(self,date):
        """
        过滤时间，大于一天的都不去爬取
        """
        nowtime=time.time()
        d1=datetime.utcfromtimestamp(nowtime)
        d2=datetime.utcfromtimestamp(date)

        return (d1-d2).days  


