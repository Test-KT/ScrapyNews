# -*- coding: utf-8 -*-
import scrapy
from SougouNews.items import SougounewsItem
import selenium
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
from datetime import datetime
import logging

class NewsSpiderSpider(scrapy.Spider):
    name = 'news_spider'
    start_urls = ['http://weixin.sogou.com/']
    req_url = 'http://weixin.sogou.com'

    logging.getLogger("requests").setLevel(logging.WARNING)
    

    def parse(self, response):
        self.initDriver()

        for i in range(7):
            if i == 0:  # 默认第一页不需要切换tag
                res = self.flipOver()
                tag_title="热门"
            else:  # 切换tag
                tag_title=self.flipTag(i)
                res=self.flipOver()

            news_box = res.xpath("//*[@id='pc_%d_0']"%(i))
            for item in news_box.css('li'):
                date = item.css('div.txt-box div.s-p span::attr(t)').extract_first()
                if self.filter_time(date) >= 1:
                    self.logger.info("time is filtered !")
                    continue

                it=self.parse_data(item,tag_title)
                yield it
                # yield response.follow(it['link'],callback=self.parse_details(response,it))

        self.closeDriver()


    # def parse_details(self,res,it):
    #     """
    #     抓取深度内容
    #     """
    #     it['']

    #     return it

    def parse_data(self,item,tag_title):
        """
        数据提取
        """
        it = SougounewsItem()
        it['title'] = item.css('div.txt-box h3 a::text').extract_first()
        it['info'] = item.css('div.txt-box p.txt-info::text').extract_first()
        it['time'] = item.css('div.txt-box div.s-p span::attr(t)').extract_first()
        it['post_user'] = item.css('div.txt-box div.s-p a::text').extract_first()
        it['link'] = item.css('div.txt-box h3 a::attr(href)').extract_first()
        it['tag']=tag_title
        return it

    def filter_time(self, date):
        """
        过滤时间，大于一天的都不去爬取
        """
        nowtime = time.time()
        d1 = datetime.utcfromtimestamp(nowtime)
        d2 = datetime.utcfromtimestamp(float(date))

        return (d1-d2).days

    def flipOver(self):
        """
        翻页，翻两页
        """
        for n in range(2):
            try:
                self.driver.find_element_by_xpath(self.look_more).click()
                self.logger.debug("click number")
                time.sleep(2)
            except Exception as e:
                self.logger.error("flipOver error")
        page_source = self.driver.page_source
        return HtmlResponse(self.req_url, body=page_source, encoding='utf-8')

    def flipTag(self,index):
        """
        切换分类
        """
        try:
            tag_link = "//*[@id='pc_%d']" % (index)
            dd=self.driver.find_element_by_xpath(tag_link)
            tag_title=dd.text
            dd.click()
            time.sleep(2)
            return tag_title
        except Exception as e:
            self.logger.error(e) 

    def initDriver(self):
        """
        初始化浏览器
        """
        self.driver=webdriver.PhantomJS()
        self.driver.get(self.req_url)
        self.driver.implicitly_wait(3)
        self.look_more = ".//div[@class='jzgd']/a"
        time.sleep(2)
        

    def closeDriver(self):
        """
        关闭浏览器
        """
        try:
            self.driver.close()
        except Exception as ex:
            pass
