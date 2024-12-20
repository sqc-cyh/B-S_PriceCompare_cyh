import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
import pandas as pd
import os

# 如果不存在目录则创建
if not os.path.exists("./data"):
    os.makedirs("./data")

# 创建edge浏览器对象
op = webdriver.EdgeOptions()
op.add_experimental_option("detach", True)
op.add_experimental_option("detach", True)  # 防止闪退
op.add_argument("disable-blink-features=AutomationControlled")  # 防止被检测, 设置一个伪装与下面的execute_cdp_cmd同效果
web = webdriver.Edge(options=op)  # 实例化一个浏览器对象
web.maximize_window()
jd_domain = "https://www.jd.com/"
jd_login_url = 'https://passport.jd.com/new/login.aspx?/'


# 判断是否存在cookie,存在则添加到浏览器，不存在则登录获取保存cookie(避免每次都需要扫码)
def is_exists_cookies():
    cookie_file = './data/jd_cookies.txt'
    if os.path.exists(cookie_file):
        # 读取cookie文件中的内容
        web.get(jd_domain)  # 添加cookie前必须打开浏览器
        time.sleep(33)
        with open(cookie_file, 'r') as file:
            # 读取文中的cookies
            cookies = json.load(file)
            # 加载cookie信息
            for cookie in cookies:
                web.add_cookie(cookie)
        print("使用已保存的cookie登录")
    else:
        web.get(jd_login_url)
        # 等待用户登录并获取cookie,
        time.sleep(30)  # 第一次登录需要用户手动登录获取cookie（扫码登录等，需要时间长点）
        dictcookies = web.get_cookies()  # 登录成功后取出cookie,格式为字典
        jsoncookies = json.dumps(dictcookies)  # 字典转json
        with open(cookie_file, 'w') as f:
            f.write(jsoncookies)  # 写入cookie文件
        print("cookies已保存")


# 滚动条缓慢下滑
def slide(web):
    # 执行这段代码，会获取到当前窗口总高度
    js = "return action=document.body.scrollHeight"
    # 初始化现在滚动条所在高度为0
    height = 0
    # 当前窗口总高度
    new_height = web.execute_script(js)

    while height < new_height:
        # 将滚动条调整至页面底部
        for i in range(height, new_height, 400):
            web.execute_script('window.scrollTo(0, {})'.format(i))
            time.sleep(0.5)
        height = new_height
        time.sleep(2)
        new_height = web.execute_script(js)


# 获取页面数据
def get_product(web):
    slide(web)  # 缓慢滑动

    html_content = web.page_source
    et = etree.HTML(html_content)
    obj_list = et.xpath('//div[@class="gl-i-wrap"]')

    for item in obj_list:
        titles = item.xpath('./div[@class="p-name p-name-type-2"]/a/em/text()')
        # print(len(titles))
        title = ""
        for i in range(len(titles)):
            title = title + titles[i]
        title = title.strip().replace("\n", "").replace(" ", "")

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
        saleses.append(sales)
        prices.append(price)
        shop_names.append(shop_name)
        urls.append(img)


# 开始爬取多页数据
def get_more(web, page):
    for i in range(1):
        print(f"爬取第{i}页数据")
        button = web.find_element(By.XPATH, '//*[@id="J_bottomPage"]/span[1]/a[9]')
        web.execute_script("arguments[0].click();", button)  # arguments[0]代表所传值element的第一个参数
        time.sleep(5)
        get_product(web)


def main():
    # 判断是否存在cookie,存在则添加到浏览器，不存在则登录获取保存cookie
    is_exists_cookies()
    web.refresh()  # 刷新网页
    time.sleep(2)
    # 发送请求并检索网页内容
    key = "小米14pro"
    search_url = f'https://search.jd.com/Search?keyword={key}'
    web.execute_script(f"window.open('{search_url}','_blank')")
    time.sleep(2)
    web.switch_to.window(web.window_handles[-1])  # 切换到最后一个标签页(新打开的页面)

    # 获取页面数据
    get_product(web)

    # 获取商品总页数
    page_num = web.find_element(By.XPATH, '//*[@id="J_bottomPage"]/span[2]/em[1]/b').text
    print(f"共计{page_num}页数据")

    # 开始爬取多页数据
    get_more(web, int(page_num) - 1)


if __name__ == '__main__':
	# 创建数据需要的空数组
    titless = []
    prices = []
    saleses = []
    urls = []
    shop_names = []
    main()

    data = {"name": titless, 'price': prices, "shop": shop_names, "sales": saleses, "img": urls}
    pd.DataFrame(data).to_csv(f'./data/京东小米手机销售.csv', index=False)

    print("全部完成")
    web.quit()

