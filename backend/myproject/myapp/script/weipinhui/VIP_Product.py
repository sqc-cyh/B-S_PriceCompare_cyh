from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from lxml import etree
import csv

class Vip_Product_Spider:
    def __init__(self, keyword):
        self.keyword = keyword
        self.start_page = 1
        self.end_page = 2
        self.options = Options()
        self.options.add_argument('--headless')  # 设置无头浏览器
        self.options.add_argument('--disable-gpu')  # 禁用GPU加速
        self.options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})  # 禁止图片加载
        self.bro = webdriver.Chrome(options=self.options)  # 使用 ChromeDriver

    def get_product_data(self):
        products_info = []
        for i in range(self.start_page, self.end_page + 1):
            url = f"https://category.vip.com/suggest.php?keyword={self.keyword}&page={i}"
            self.bro.get(url)
            sleep(3)
            self.bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            sleep(3)
            products_info.extend(self.parse_data())
        self.bro.quit()
        return products_info

    def parse_data(self):
        html = etree.HTML(self.bro.page_source)
        div_list = html.xpath('//section[@class="goods-list c-goods-list--normal"]/div')[1:]
        products = []
        for div in div_list:
            dic={}
            sleep(0.5)
            try:
                dic["title"]=div.xpath('.//div[@class="c-goods-item__name  c-goods-item__name--two-line"]/text()')[0]
            except:
                dic["title"]=""
            try:
                dic["price"]=div.xpath('.//div[@class="c-goods-item__sale-price J-goods-item__sale-price"]//text()')[1]
            except:
                dic["price"]=""
            try:
                dic["market_price"]=div.xpath('.//div[@class="c-goods-item__market-price  J-goods-item__market-price"]//text()')[1]
            except:
                dic["market_price"]=""
            try:
                dic["discount"]=div.xpath('.//div[@class="c-goods-item__discount  J-goods-item__discount"]/text()')[0]
            except:
                dic["discount"]=""
            try:
                dic["img_link"]="http:"+div.xpath('.//img[@class="J-goods-item__img"]/@src')[0]
            except:
                dic["img_link"]=""
            try:
                dic["details_link"]="https:"+div.xpath('.//a[@target="_blank"]/@href')[0]
            except:
                dic["details_link"]=""
            products.append(dic)
        print(products)
        return products