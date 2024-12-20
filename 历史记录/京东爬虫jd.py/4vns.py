from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from lxml import etree
import csv

class JD_Product_Spider():
    def __init__(self):
        self.keyword = input("请输入要采集商品的关键字：")  # 商品的关键字
        self.options = Options()
        self.options.add_argument('--headless')  # 设置无头浏览器
        self.options.add_argument('--disable-gpu')  # 禁用GPU加速
        self.options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})  # 禁止图片加载
        self.bro = webdriver.Edge(options=self.options)

    def parser_product_data(self):
        html = etree.HTML(self.bro.page_source)
        li_list = html.xpath('//ul[@class="gl-warp clearfix"]/li')
        with open("./jd.csv", "a+", encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["title", "commit", "shop", "price", "details", "productid"])
            if f.tell() == 0:
                writer.writeheader()
            for li in li_list:
                # print(li)
                dic = {}
                try:
                    dic["title"] = "".join(li.xpath('./div/div[@class="p-name p-name-type-2"]/a/em//text()')).replace("\n", "")
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
                try:
                    dic["img_link"] = "https:" + li.xpath('.//div[@class="p-img"]/a/img/@src')
                except:
                    dic["img_link"] = ""
                writer.writerow(dic)

    def get_product_data(self):
        self.bro.maximize_window()  # 最大化浏览器
        url = f"https://search.jd.com/Search?keyword={self.keyword}&enc=utf-8"
        self.bro.get(url)
        self.bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下滑动一屏
        sleep(1)
        try:
            page = self.bro.find_element(By.XPATH, '//span[@class="p-skip"]/em/b').text
            print(f"{self.keyword}检索到共{page}页数据")
        except Exception as e:
            print(f"无法获取总页数：{e}")
            page = 1  # 如果无法获取页数，则默认为1页

        start_page = input("请输入起始页数：")
        end_page = input("请输入结束页数：")
        for i in range(int(start_page), int(end_page) + 1):
            sleep(1)
            print("-" * 30 + f"已获取第{i}页数据" + "-" * 30)
            url = f"https://search.jd.com/Search?keyword={self.keyword}&page={i}&enc=utf-8"
            self.bro.get(url)
            self.parser_product_data()
        self.bro.quit()

if __name__ == "__main__":
    spider = JD_Product_Spider()
    spider.get_product_data()