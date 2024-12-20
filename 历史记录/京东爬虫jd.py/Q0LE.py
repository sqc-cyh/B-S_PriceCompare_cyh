from selenium import webdriver
from selenium.webdriver.edge.options import Options
from time import sleep
from lxml import etree
import csv

options = Options()
options.add_argument('--headless=old')
driver = webdriver.Edge(options=options)
class JD_Product_Spider():
    def __init__(self):
        self.keyword = input("请输入要采集商品的关键字：")  # 商品的关键字
        self.options = Options()
        self.options.add_argument('--headless')  # 设置无头浏览器
        self.options.add_argument('--disable-gpu')  # 禁用GPU加速
        self.options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})  # 禁止图片加载，加快速度
        self.bro = webdriver.Edge(options=self.options)
        self.bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })  # 可能失效

    def Parser_Profuct_Data(self):
        html = etree.HTML(self.bro.page_source)
        li_list = html.xpath('//ul[@class="gl-warp clearfix"]/li')
        with open("./jd.csv", "a+", encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["title", "commit", "shop", "price", "details", "productid"])
            if f.tell() == 0:
                writer.writeheader()
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
                writer.writerow(dic)

    def Get_Product_Data(self):
        self.bro.maximize_window()  # 最大化浏览器
        url = f"https://search.jd.com/Search?keyword={self.keyword}&enc=utf-8"
        self.bro.get(url)
        self.bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下滑动一屏
        sleep(1)
        self.Parser_Profuct_Data()  # 解析第一页数据
        self.bro.quit()

if __name__ == "__main__":
    Spider = JD_Product_Spider()
    Spider.Get_Product_Data()