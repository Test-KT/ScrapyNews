# encoding=utf-8
import random
from SougouNews.user_agents import agents

from selenium import webdriver
import time
from scrapy.http import HtmlResponse 


class UserAgentMiddleware(object):
    def process_request(self,request,spider):
        agent=random.choice(agents)
        request.headers["User-Agent"]=agent

class SeleniumMiddleware(object):
    def process_request(self,request,spider):
        url='http://weixin.sogou.com'
        if request.url==url:
            try:
                driver=webdriver.PhantomJS()
                driver.implicitly_wait(3)
                look_more=".//div[@class='jzgd']/a"
                for i in range(3):
                    driver.find_element_by_xpath(look_more)
                    print('click number')
                    time.sleep(3)
                
                page_source=driver.page_source
                driver.close()

                res=HtmlResponse(request.url,body=page_source,encoding='utf-8',request=request)
                
                return res


            except Exception as e:
                pass
            
                
        else:
            None