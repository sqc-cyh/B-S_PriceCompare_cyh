from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from time import sleep
from lxml import etree
import csv

class JD_Product_Spider():
    def __init__(self):
        self.keyword = input("请输入要采集商品的关键字：")  # 商品的关键字
        option = Options()
        option.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})  # 禁止图片加载，加快速度
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')  # 设置无头浏览器
        self.bro = webdriver.Edge(options=option)

    def Parser_Profuct_Data(self):
        html = etree.HTML(self.bro.page_source)
        li_list = html.xpath('//ul[@class="gl-warp clearfix"]/li')
        for li in li_list:
            dic = {}
            try:
                dic["title"] = li.xpath('./div/div[@class="p-name p-name-type-2"]/a/em//text()')
            except:
                dic["title"] = ""
            try:
                dic["commit"] = li.xpath('./div/div[@class="p-commit"]/strong/a/text()')[0]
            except:
                dic["commit"] = ""
            try:
                dic["shop"] = li.xpath('./div/div[@class="p-shop"]/span/a/text()')[0]
            except:
                dic["shop"] = ""
            try:
                dic["price"] = li.xpath('./div/div[@class="p-price"]/strong/i/text()')[0]
            except:
                dic["price"] = ""
            try:
                dic["details"] = "https:" + li.xpath('./div/div[@class="p-name p-name-type-2"]/a/@href')[0]
            except:
                dic["details"] = ""
            try:
                dic["productid"] = li.xpath('./@data-sku')[0]
            except:
                dic["productid"] = ""
            with open("./jd.csv", "a+", encoding="utf-8") as f:
                writer = csv.DictWriter(f, dic.keys())
                writer.writerow(dic)

    def Get_Product_Data(self):
        self.bro.maximize_window()  # 最大化浏览器
        url = f"https://search.jd.com/Search?keyword={self.keyword}&"
        self.bro.get(url)
        self.bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下滑动一屏

        # 使用显式等待确保页面加载完成
        wait = WebDriverWait(self.bro, 10)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="p-skip"]/em/b')))
            page = self.bro.find_element_by_xpath('//span[@class="p-skip"]/em/b').text
            print(f"{self.keyword}检索到共{page}页数据")
        except:
            print("无法获取总页数")
            return

        start_page = input("请输入起始页数：")
        end_page = input("请输入结束页数：")
        for i in range(int(start_page), int(end_page) + 1):
            sleep(1)
            print(f"-" * 30 + f"已获取第{i}页数据" + "-" * 30)
            url = f"https://search.jd.com/Search?keyword={self.keyword}&page={i * 2 - 1}&"
            self.bro.get(url)
            self.Parser_Profuct_Data()
        self.bro.quit()

if __name__ == "__main__":
    Spider = JD_Product_Spider()
    Spider.Get_Product_Data()