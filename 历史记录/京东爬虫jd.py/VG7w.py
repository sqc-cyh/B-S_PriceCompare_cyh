import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 初始化webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

# 导航至亚马逊热卖榜页面
url = 'https://www.amazon.com/Best-Sellers/zgbs'
driver.get(url)
time.sleep(5)  # 等待页面加载完成

# 抓取数据
data = []
while True:
    wait = WebDriverWait(driver, 10)
    products = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="zg-item-immersion"]')))
    
    for product in products:
        try:
            name = product.find_element_by_xpath('.//span[@class="p13n-sc-truncated"]').text
        except:
            name = None
        try:
            price = product.find_element_by_xpath('.//span[@class="p13n-sc-price"]').text
        except:
            price = None
        try:
            rating = product.find_element_by_xpath('.//span[@class="a-icon-alt"]').text
        except:
            rating = None
        
        data.append({'name': name, 'price': price, 'rating': rating})
    
    try:
        next_button = driver.find_element_by_xpath('//li[@class="a-last"]/a')
        next_button.click()
        time.sleep(random.uniform(2, 5))  # 随机延迟
    except:
        break  # 没有更多页面，退出循环

# 保存数据
df = pd.DataFrame(data)
df.to_csv('amazon_best_sellers.csv', index=False)

# 清理数据
df['price'] = df['price'].str.replace('$', '').astype(float)
df['rating'] = df['rating'].str.extract(r'(\d+\.\d+)').astype(float)
