from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from lxml import etree
import csv
import re
import os

class Suning_Product_Spider():
    def __init__(self):
        self.keyword = input("请输入要采集商品的关键字：")  # 商品的关键字
        self.options = Options()
        self.options.add_argument('--headless')  # 设置无头浏览器
        self.options.add_argument('--disable-gpu')  # 禁用GPU硬件加速
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})  # 禁止图片加载
        self.browser = webdriver.Edge(options=self.options)
        # 获取当前脚本文件的目录
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def get_comment_data(self):
        self.browser.get(f'https://search.suning.com/{self.keyword}/')  
        product_list = []  # 用于存储产品数据
        try:
            page_element = self.browser.find_element(By.XPATH, '//span[@class="page-more"]')
            page = page_element.text
            page = re.findall('(\d+)', page)[0]
            print(f"{self.keyword}共检索到{int(page)}页数据")
            self.start_page = 1  # 自动获取前10页数据
            self.end_page = min(10, int(page))
            for i in range(self.start_page, self.end_page + 1):
                sleep(4)
                self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下滑动一屏
                sleep(4)
                products = self.parse_product_data()  # 获取当前页面的产品数据
                product_list.extend(products)  # 添加到总列表
                sleep(4)
                if i < self.end_page:  # 如果不是最后一页，则翻页
                    page_input_element = self.browser.find_element(By.XPATH, '//span[@class="page-more"]/input')
                    page_input_element.clear()
                    page_input_element.send_keys(str(i + 1))
                    sleep(4)
                    next_button = self.browser.find_element(By.XPATH, '//a[@class="page-more ensure"]')
                    self.browser.execute_script("arguments[0].click();", next_button)  # 点击确认
        finally:
            self.browser.quit()
        return product_list  # 返回爬取的产品数据

    def parse_product_data(self):
        html = etree.HTML(self.browser.page_source)
        li_list = html.xpath('//ul[@class="general clearfix"]/li')
        product_data = []  # 存储当前页面的产品数据

        for li in li_list:
            dic = {}
            try:
                dic["title"] = "".join(li.xpath('.//div[@class="res-info"]/div[@class="title-selling-point"]/a[1]//text()')).replace("\n", "")
            except:
                dic["title"] = ""
            try:
                dic["price"] = "".join(li.xpath('.//div[@class="price-box"]/span[1]//text()')).replace("\n", "")
            except:
                dic["price"] = ""
            try:
                dic["img_link"] = "http:" + li.xpath('.//div[@class="img-block"]/a[1]/img/@src')[0]
            except:
                dic["img_link"] = ""

            product_data.append(dic)  # 添加当前产品数据到列表
        
        return product_data  # 返回当前页面的产品数据

if __name__ == '__main__':
    spider = Suning_Product_Spider()
    spider.get_comment_data()