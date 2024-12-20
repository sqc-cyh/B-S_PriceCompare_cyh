from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from lxml import etree
import csv
import re

class Suning_Product_Spider():
    def __init__(self):
        self.keyword = input("请输入要采集商品的关键字：")  # 商品的关键字
        self.options = Options()
        self.options.add_argument('--headless')  # 设置无头浏览器
        self.options.add_argument('--disable-gpu')  # 禁用GPU硬件加速
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})  # 禁止图片加载
        self.browser = webdriver.Edge(options=self.options)

    def get_comment_data(self):
        self.browser.get(f'https://search.suning.com/{self.keyword}/')  # 修复 URL 拼接
        try:
            page_element = self.browser.find_element(By.XPATH, '//span[@class="page-more"]')
            page = page_element.text
            page = re.findall('(\d+)', page)[0]
            print(f"{self.keyword}共检索到{int(page)}页数据")
            self.start_page = input("请输入起始页数：")
            self.end_page = input("请输入结束页数：")
            for i in range(int(self.start_page), int(self.end_page) + 1):
                sleep(4)
                self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下滑动一屏
                sleep(4)
                self.parse_product_data()
                sleep(4)
                page_input_element = self.browser.find_element(By.XPATH, '//span[@class="page-more"]/input')
                page_input_element.send_keys(str(i))  # 输入页数
                sleep(4)
                next_button = self.browser.find_element(By.XPATH, '//a[@class="page-more ensure"]')
                self.browser.execute_script("arguments[0].click();", next_button)  # 点击确认
        finally:
            self.browser.quit()

    def parse_product_data(self):
        html = etree.HTML(self.browser.page_source)
        li_list = html.xpath('//ul[@class="general clearfix"]/li')
        field_names = ["title", "price", "type", "comment_num", "shop", "label", "img_link", "detail_link"]  # 定义字段名称
        with open("./suning.csv", "a+", encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            if f.tell() == 0:  # 如果文件是新的，则写入表头
                writer.writeheader()
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
                    dic["type"] = li.xpath('.//div[@class="info-config"]/@title')[0]
                except:
                    dic["type"] = ""
                try:
                    dic["comment_num"] = ''.join(li.xpath('.//div[@class="info-evaluate"]/a[1]//text()'))
                except:
                    dic["comment_num"] = ""
                try:
                    dic["shop"] = li.xpath('.//div[@class="store-stock"]/a[1]/text()')[0]
                except:
                    dic["shop"] = ""
                try:
                    dic["label"] = ','.join(li.xpath('.//div[@class="sales-label"]//text()'))
                except:
                    dic["label"] = ""
                try:
                    dic["img_link"] = "http:" + li.xpath('.//div[@class="img-block"]/a[1]/img/@src')[0]
                except:
                    dic["img_link"] = ""
                try:
                    if "http" in li.xpath('.//div[@class="res-info"]/div[@class="title-selling-point"]/a[1]/@href')[0]:
                        dic["detail_link"] = li.xpath('.//div[@class="res-info"]/div[@class="title-selling-point"]/a[1]/@href')[0]
                    else:
                        dic["detail_link"] = "http:" + li.xpath('.//div[@class="res-info"]/div[@class="title-selling-point"]/a[1]/@href')[0]
                except:
                    dic["detail_link"] = ""
                writer.writerow(dic)

if __name__ == '__main__':
    spider = Suning_Product_Spider()
    spider.get_comment_data()