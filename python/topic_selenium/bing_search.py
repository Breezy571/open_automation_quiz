import time
from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

my_name = 'Breezy'
next_key = 'Selenium'
url = 'https://www.bing.com/?mkt=zh-CN'
# 初始化WebDriver
driver = webdriver.Chrome()

# 打开测试网站
driver.get(url)

# 搜索关键词"您的姓名"
search_box = driver.find_element(By.NAME, "q")
search_box.clear()
search_box.send_keys(my_name)
search_box.send_keys(Keys.RETURN)
# 等待页面加载
time.sleep(3)

# 获取第二页的链接
wait = WebDriverWait(driver, 10)
next_page = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                   f"//a[@class='sb_pagN sb_pagN_bp b_widePag sb_bp ' and @aria-label='下一页' and @title='下一页']")))
next_page.click()
# 等待页面加载
time.sleep(3)


# 打印搜索结果并统计TLD
def print_search_results():
    # 先找到id为b_results的ol元素
    ol_element = driver.find_element(By.ID, "b_results")

    # 再在该ol元素下查找所有的a标签元素
    results = ol_element.find_elements(By.TAG_NAME, "a")

    tld_count = defaultdict(int)

    for result in results:
        title = result.accessible_name
        link = result.get_attribute('href')
        if link is None or title is None:
            continue
        print(f"{title} --> {link}")

        # 统计顶级域名
        domain = link.split('/')[2]
        second_level_domain = domain.split('.')[-2:]
        tld = '.'.join(second_level_domain)
        tld_count[tld] += 1

    # 打印TLD统计
    print("\n结果统计")
    for tld, count in tld_count.items():
        print(f"{tld} --> {count}")

print(f"结果列表 ({my_name})")
print_search_results()

# 搜索关键词"Selenium"
search_box = driver.find_element(By.NAME, "q")
search_box.clear()
search_box.send_keys(next_key)
search_box.send_keys(Keys.RETURN)

time.sleep(3)

# 获取第二页的链接
wait = WebDriverWait(driver, 10)
next_page = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                   f"//a[@class='sb_pagN sb_pagN_bp b_widePag sb_bp ' and @aria-label='下一页' and @title='下一页']")))
next_page.click()
time.sleep(3)

# 执行打印并统计"Selenium"搜索结果
print(f"\n结果列表 ({next_key})")
print_search_results()

# 关闭浏览器
driver.quit()
