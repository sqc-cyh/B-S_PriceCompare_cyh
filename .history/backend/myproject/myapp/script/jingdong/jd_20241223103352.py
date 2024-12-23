import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
import pandas as pd
import os
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 如果不存在目录则创建
if not os.path.exists("./data"):
    os.makedirs("./data")
current_dir = os.path.dirname(os.path.abspath(__file__))
# 创建edge浏览器对象
op = webdriver.EdgeOptions()
op.add_experimental_option("detach", True)  # 不需要分离窗口
op.add_argument("disable-blink-features=AutomationControlled")  # 防止被检测
op.add_argument("--headless")  # 启用无头模式
op.add_argument("--no-sandbox")  # 解决权限问题
op.add_argument("--enable-unsafe-swiftshader")  # 添加这个参数
web = webdriver.Edge(options=op)  # 实例化一个浏览器对象
# web = webdriver.Edge(options=op)  # 实例化一个浏览器对象
# web.maximize_window()
print('newnewnewnew')
# 判断是否存在cookie,存在则添加到浏览器，不存在则登录获取保存cookie(避免每次都需要扫码)
def is_exists_cookies(cookie_file):
    if os.path.exists(cookie_file):
        # 读取cookie文件中的内容
        web.get("https://www.jd.com/")  # 添加cookie前必须打开浏览器
        time.sleep(2)
        with open(cookie_file, 'r') as file:
            # 读取文中的cookies
            cookies = json.load(file)
            # 加载cookie信息
            for cookie in cookies:
                web.add_cookie(cookie)
        print("使用已保存的cookie登录")
    else:
        print("未找到cookie文件，将使用新会话")

# 滚动条缓慢下滑
def slide(web):
    js = "return document.body.scrollHeight"
    height = 0
    new_height = web.execute_script(js)
    while height < new_height:
        for i in range(height, new_height, 400):
            web.execute_script('window.scrollTo(0, {})'.format(i))
            time.sleep(0.5)
        height = new_height
        time.sleep(2)
        new_height = web.execute_script(js)

# 获取页面数据
def get_product(web):
    slide(web)
    html_content = web.page_source
    et = etree.HTML(html_content)
    obj_list = et.xpath('//div[@class="gl-i-wrap"]')
    titless, prices, saleses, shop_names, urls = [], [], [], [], []
    for item in obj_list:
        titles = item.xpath('./div[@class="p-name p-name-type-2"]/a/em/text()')
        title = "".join(titles).strip().replace("\n", "").replace(" ", "")
        price_head = item.xpath('./div[@class="p-price"]/*/em/text()')[0]
        price_body = item.xpath('./div[@class="p-price"]/*/i/text()')[0]
        price = price_head + price_body
        shop_name = item.xpath('./div[@class="p-shop"]/span/a/text()')[0]
        sales1 = item.xpath('./div[@class="p-commit"]/strong/a/text()')[0]
        sales2 = item.xpath('./div[@class="p-commit"]/strong/text()')[0]
        sales = sales1 + sales2
        img_elements = item.xpath('./div[@class="p-img"]/a/img/@src')
        img = img_elements[0] if img_elements else ''
        if not img.startswith('http'):
            img = 'https:' + img
        titless.append(title)
        prices.append(price)
        saleses.append(sales)
        shop_names.append(shop_name)
        urls.append(img)
    return titless, prices, saleses, shop_names, urls

# 开始爬取多页数据
def get_more(web, page_num, titless, prices, saleses, shop_names, urls):
    for i in range(1):
        print(f"爬取第{i+1}页数据")
        WebDriverWait(web, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="J_bottomPage"]/span[1]/a[9]'))).click()
        time.sleep(5)  # 等待新页面加载
        t, p, s, sn, u = get_product(web)
        titless.extend(t)
        prices.extend(p)
        saleses.extend(s)
        shop_names.extend(sn)
        urls.extend(u)
def main():
    titless, prices, saleses, shop_names, urls = [], [], [], [], []
    if len(sys.argv) < 2:
        print("请提供搜索关键词")
        return

    key = sys.argv[1]  # 从命令行获取搜索关键词
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)
    cookie_file = current_dir + r'/data/jd_cookies.txt'
    print(cookie_file)
    is_exists_cookies(cookie_file)
    search_url = f'https://search.jd.com/Search?keyword={key}'
    web.execute_script(f"window.open('{search_url}','_blank')")
    time.sleep(2)
    web.switch_to.window(web.window_handles[-1])
    page_num = int(web.find_element(By.XPATH, '//*[@id="J_bottomPage"]/span[2]/em[1]/b').text)
    print(f"共计{page_num}页数据")
    get_more(web, page_num, titless, prices, saleses, shop_names, urls)
    data = {"name": titless, 'price': prices, "shop": shop_names, "sales": saleses, "img": urls}
    csv_file_path = os.path.join(current_dir, 'data', f'京东{key}销售.csv')
    print("保存CSV文件到:", csv_file_path)
    pd.DataFrame(data).to_csv(csv_file_path, index=False)
    print("全部完成")
    # print(data)
    web.quit()

if __name__ == '__main__':
    main()