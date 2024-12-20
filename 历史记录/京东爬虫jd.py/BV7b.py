from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time
import random
import csv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import os
import requests
from datetime import datetime
import re

KEYWORD = '美妆'
CSV_FILE = 'DepartmentStore.csv'
id = 3538
dratenums = 5
drate = 5
num = 5

# 创建EdgeOptions对象
options = Options()

# 设置Edge WebDriver的路径
webdriver_path = 'G:\\大三下暑期实训基于电商商品推荐平台\\爬虫\\a\\msedgedriver.exe'
service = Service(webdriver_path)

# 初始化Edge WebDriver
driver = webdriver.Edge(service=service, options=options)

# 窗口最大化
driver.maximize_window()

wait = WebDriverWait(driver, 15)

def search_goods(start_page, total_pages):
    print('正在搜索: ')
    try:
        driver.get('https://www.taobao.com')
        time.sleep(10)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                               {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys(KEYWORD)
        submit.click()
        time.sleep(10)

        if start_page != 1:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            random_sleep(1, 3)
            pageInput = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/div[1]/div[2]/div[4]/div/div/span[3]/input')))
            pageInput.send_keys(start_page)
            admit = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/div[1]/div[2]/div[4]/div/div/button[3]')))
            admit.click()

        get_goods()

        for i in range(start_page + 1, start_page + total_pages):
            page_turning(i)
    except TimeoutException:
        print("search_goods: error")
        return search_goods(start_page, total_pages)

def page_turning(page_number):
    print('正在翻页: ', page_number)
    try:
        submit = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="sortBarWrap"]/div[1]/div[2]/div[2]/div[8]/div/button[2]')))
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.XPATH, '//*[@id="sortBarWrap"]/div[1]/div[2]/div[2]/div[8]/div/span/em'), str(page_number)))
        get_goods()
    except TimeoutException:
        page_turning(page_number)

def random_sleep(timeS, timeE):
    random_sleep_time = random.uniform(timeS, timeE)
    time.sleep(random_sleep_time)

def scroll_smoothly(duration):
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    steps = 30  # 分成30步
    step_duration = duration / steps  # 每步的时间
    step_height = (total_height - viewport_height) / steps  # 每步的高度

    for i in range(steps):
        driver.execute_script(f"window.scrollBy(0, {step_height});")
        time.sleep(step_duration)

def get_goods():
    global id, drate, dratenums, num  # 声明使用全局变量 id
    random_sleep(2, 4)
    # 滑动浏览器滚轮，向下滑动
    scroll_smoothly(4)
    random_sleep(4, 4)  # 等待页面加载
    html = driver.page_source
    doc = pq(html)
    items = doc(
        'div.PageContent--contentWrap--mep7AEm > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Content--content--sgSCZ12 > div > div').items()

    for item in items:
        title = item.find('.Title--title--jCOPvpf span').text()
        price_int = item.find('.Price--priceInt--ZlsSi_M').text()
        price_float = item.find('.Price--priceFloat--h2RR0RK').text()
        if price_int and price_float:
            price = float(f"{price_int}{price_float}")
        else:
            price = 0.0
        deal = item.find('.Price--realSales--FhTZc7U').text()
        location = item.find('.Price--procity--_7Vt3mX').text()
        shop = item.find('.ShopInfo--TextAndPic--yH0AZfx a').text()
        postText = item.find('.SalesPoint--subIconWrapper--s6vanNY span').text()
        result = 1 if "包邮" in postText else 0
        image = item.find('.MainPic--mainPicWrapper--iv9Yv90 img').attr('src')
        # 图片的URL
        image_url = image
        pattern = r"https:\/\/.*?\.jpg"

        match = re.search(pattern, image_url)
        if match:
            print("Extracted URL:", match.group(0))
        else:
            print("No match found")
        image_url = match.group(0)

        # 保存图片的文件夹
        save_folder = "shopping_cover"

        # 确保保存路径存在
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # 将图片文件名固定为 '1.jpg'
        image_name = str(id) + ".jpg"

        # 完整的保存路径
        save_path = os.path.join(save_folder, image_name)

        # 获取当前日期
        current_date = datetime.now()

        # 格式化日期为 'yyyy-mm-dd'
        formatted_date = current_date.strftime('%Y-%m-%d')

        imdblink = item.find('.Card--doubleCardWrapper--L2XFE73 a').attr('href')

        # 下载图片并保存
        try:
            with requests.get(image_url, stream=True) as response:
                response.raise_for_status()
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
            print(f"图片已保存到: {save_path}")
            product = {
                'id': id,
                'name': title,
                'director': shop,
                'country': location,
                'years': formatted_date,
                'leader': price,
                'd_rate_nums': dratenums,
                'd_rate': drate,
                'intro': deal + str(result),
                'num': num,
                'orign_image_link': image,
                'image_link': save_folder + '/' + image_name,
                'imdb_link': imdblink
            }
            save_to_csv(product)
            id += 1
        except requests.RequestException as e:
            print(f"下载图片失败：{e}")

        # 直接滑动浏览器滚轮到最顶部
        driver.execute_script("window.scrollTo(0, 0);")

def save_to_csv(result):
    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([result['id'], result['name'], result['director'], result['country'], result['years'], result['leader'], result['d_rate_nums'], result['d_rate'], result['intro'], result['num'], result['orign_image_link'], result['image_link'], result['imdb_link']])
        print('存储到CSV成功: ', result)
    except Exception as e:
        print('存储到CSV出错: ', result, e)

def main():
    try:
        # 检查文件是否存在，如果不存在则创建并写入标题行
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'name', 'director', 'country', 'years', 'leader', 'd_rate_nums', 'd_rate', 'intro', 'num', 'orign_image_link', 'image_link', 'imdb_link'])

        pageStart = int(input("输入您想开始爬取的页面数: "))
        pageAll = int(input("输入您想爬取的总页面数: "))
        search_goods(pageStart, pageAll)
    except Exception as e:
        print('main函数报错: ', e)

if __name__ == '__main__':
    main()

