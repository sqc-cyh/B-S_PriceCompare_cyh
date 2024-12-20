import decimal
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from lxml import etree
import re
import os

class Suning_Product_Spider():
    def __init__(self, keyword):  
        self.keyword = keyword  
        self.options = Options()
        self.options.add_argument('--headless')  
        self.options.add_argument('--disable-gpu')  
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})  
        self.browser = webdriver.Edge(options=self.options)
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def get_comment_data(self):
        self.browser.get(f'https://search.suning.com/{self.keyword}/')    
        product_list = []  
        try:
            # 直接获取第一页的数据，不需要翻页
            sleep(2)  # 等待页面加载
            products = self.parse_product_data()  
            if len(products) >= 30:  # 只爬取前30条数据
                product_list.extend(products[:30])
            else:
                product_list.extend(products)
        finally:
            self.browser.quit()
        return product_list  

    def clean_price(self, price_str):
        try:
            return decimal.Decimal(re.sub(r'[^\d.]', '', price_str))
        except decimal.InvalidOperation:
            return None

    def parse_product_data(self):
        html = etree.HTML(self.browser.page_source)
        li_list = html.xpath('//ul[@class="general clearfix"]/li')
        product_data = []  

        # 只处理前30个商品
        for li in li_list[:30]:
            dic = {}
            try:
                dic["title"] = "".join(li.xpath('.//div[@class="res-info"]/div[@class="title-selling-point"]/a[1]//text()')).replace("\n", "")
            except:
                dic["title"] = ""
            try:
                price_str = "".join(li.xpath('.//div[@class="price-box"]/span[1]//text()')).replace("\n", "")
                dic["price"] = self.clean_price(price_str)  
            except:
                dic["price"] = ""
            try:
                dic["img_link"] = "http:" + li.xpath('.//div[@class="img-block"]/a[1]/img/@src')[0]
            except:
                dic["img_link"] = ""

            product_data.append(dic)
        
        return product_data  