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
        self.browser.get(f'https://search.suning.com/{self.keyword}/')  
        try:
            page_element = self.browser.find_element(By.XPATH, '//span[@class="page-more"]')
            page = page_element.text
            page = re.findall('(\d+)', page)[0]
            print(f"{self.keyword}共检索到{int(page)}页数据")
            # 设置自动获取前10页数据
            self.start_page = 1
            self.end_page = min(10, int(page))  # 确保不超过总页数
            for i in range(self.start_page, self.end_page + 1):
                sleep(4)
                self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下滑动一屏
                sleep(4)
                self.parse_product_data()
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

    def parse_product_data(self):
        html = etree.HTML(self.browser.page_source)
        li_list = html.xpath('//ul[@class="general clearfix"]/li')
        field_names = ["title", "price", "type", "comment_num", "shop", "label", "img_link", "detail_link"]  # 定义字段名称
        with open(f"./suning_{self.keyword}.csv", "a+", encoding="utf-8", newline='') as f:
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