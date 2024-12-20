from selenium import webdriver
from selenium.webdriver import EdgeOptions
from time import sleep
from lxml import etree
import csv

class JD_Product_Spider():
    def __init__(self):
        self.keyword = input("请输入要采集商品的关键字：")  # 商品的关键字
        option = EdgeOptions()
        option.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})  # 禁止图片加载，加快速度
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')  # 设置无头浏览器
        self.bro = webdriver.Edge(options=option)
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
        for li in li_list:
            dic = {}
            try:
                dic["title"] = li.xpath('./div/div[@class="p-name p-name-type-2"]/a/em//text()')[0]
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
                writer = csv.DictWriter(f, fieldnames=dic.keys())
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerow(dic)

    def Get_Product_Data(self):
        self.bro.maximize_window()  # 最大化浏览器
        url = "https://search.jd.com/Search?keyword=%s" % self.keyword
        self.bro.get(url)
        self.bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下滑动一屏
        sleep(1)
        try:
            page = self.bro.find_element_by_xpath('//span[@class="p-skip"]/em/b').text
            print("%s检索到共%s页数据" % (self.keyword, page))
        except:
            print("无法获取页数，可能是页面结构变化或网络问题")
            return
        start_page = input("请输入起始页数：")
        end_page = input("请输入结束页数：")
        for i in range(int(start_page), int(end_page) + 1):
            sleep(1)
            print("-" * 30 + "已获取第%s页数据" % (i) + "-" * 30)
            url = "https://search.jd.com/Search?keyword=%s&page=%d" % (self.keyword, i)
            self.bro.get(url)
            self.Parser_Profuct_Data()
        self.bro.quit()

if __name__ == "__main__":
    Spider = JD_Product_Spider()
    Spider.Get_Product_Data()