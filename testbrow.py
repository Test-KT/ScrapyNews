import selenium
from selenium import webdriver
import time
import scrapy
from scrapy.http import HtmlResponse


driver = webdriver.PhantomJS()
# driver = webdriver.Chrome()
driver.get("http://weixin.sogou.com/")
driver.implicitly_wait(3)

time.sleep(4)
look_more = ".//div[@class='jzgd']/a"

for n in range(2):
    driver.find_element_by_xpath(look_more).click()
    print("click number")
    time.sleep(2)
page_source=driver.page_source 
res=HtmlResponse("http://weixin.sogou.com",body=page_source,encoding='utf-8')
box=res.css('ul.news-list')
items=box.css('li')
print(len(items))

driver.close()
