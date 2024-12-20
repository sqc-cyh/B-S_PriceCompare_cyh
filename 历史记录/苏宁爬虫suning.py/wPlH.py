from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from lxml import etree
import csv

class Vip_Product_Spider:
    def __init__(self, keyword, start_page, end_page):
        self.keyword = keyword
        self.start_page = int(start_page)
        self.end_page = int(end_page)
        self.options = Options()
        self.options.add_argument('--headless')  # 设置无头浏览器
        self.options.add_argument('--disable-gpu')  # 禁用GPU加速
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})  # 禁止图片加载
        self.bro = webdriver.Edge(options=self.options)

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
            product = {
                "title": div.xpath('.//div[@class="c-goods-item__name c-goods-item__name--two-line"]/text()')[0] if div.xpath('.//div[@class="c-goods-item__name c-goods-item__name--two-line"]/text()') else "",
                "sale_price": div.xpath('.//div[@class="c-goods-item__sale-price J-goods-item__sale-price"]//text()')[1] if div.xpath('.//div[@class="c-goods-item__sale-price J-goods-item__sale-price"]//text()') else "",
                "market_price": div.xpath('.//div[@class="c-goods-item__market-price J-goods-item__market-price"]//text()')[1] if div.xpath('.//div[@class="c-goods-item__market-price J-goods-item__market-price"]//text()') else "",
                "discount": div.xpath('.//div[@class="c-goods-item__discount J-goods-item__discount"]/text()')[0] if div.xpath('.//div[@class="c-goods-item__discount J-goods-item__discount"]/text()') else "",
                "img_link": 'https:' + div.xpath('.//img[@class="J-goods-item__img"]/@src')[0] if div.xpath('.//img[@class="J-goods-item__img"]/@src') else "",
                "details_link": 'https:' + div.xpath('.//a[@target="_blank"]/@href')[0] if div.xpath('.//a[@target="_blank"]/@href') else "",
            }
            products.append(product)
        return products

# Example usage in Django view
def search(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        search_query = body.get('query')
        platform = body.get('platform')
        start_page = body.get('start_page', 1)
        end_page = body.get('end_page', 1)

        if not search_query:
            return JsonResponse({'message': '搜索内容不能为空'}, status=400)

        spiders = {
            'vip': Vip_Product_Spider,
            # 'suning': Suning_Product_Spider,
            # 'jd': JD_Product_Spider,
        }
        SpiderClass = spiders.get(platform)
        if not SpiderClass:
            return JsonResponse({'message': '不支持的平台'}, status=400)

        spider = SpiderClass(search_query, start_page, end_page)
        products = spider.get_product_data()

        # Process products as needed, e.g., save to database

        results = [
            {
                'title': prod['title'],
                'sale_price': prod['sale_price'],
                'market_price': prod['market_price'],
                'discount': prod['discount'],
                'img_link': prod['img_link'],
                'details_link': prod['details_link'],
            } for prod in products
        ]
        return JsonResponse({'results': results}, status=200)

    return JsonResponse({'message': '仅支持 POST 请求'}, status=405)