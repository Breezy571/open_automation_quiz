import os

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://jinshuju.net/templates/detail/Dv9JPD"

browser = os.environ.get('BROWSER_TYPE')
if browser is None:
    browser = 'chrome'
print(f'使用{browser}浏览器')

if not os.path.exists('screenshots'):
    os.mkdir('screenshots')
# Feature 文件路径
scenarios("./apply.feature", features_base_dir=".")


@pytest.fixture
def driver():
    if browser == 'edge':
        driver = webdriver.Edge()
    else:
        driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@given(parsers.parse('打开网页 "{page_title}"'))
def open_page(driver, page_title):
    driver.get(url)
    assert page_title in driver.title


@when(parsers.parse('在第一页填写以下内容:\n{datatable}'))
def fill_first_page(driver, datatable):
    data = parse_datatable(datatable)

    iframe_xpath = '//iframe[@class="TemplatePreview_iframe__Ep1Or"]'

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, iframe_xpath))
    )

    iframe = driver.find_element(By.XPATH, iframe_xpath)
    driver.switch_to.frame(iframe)

    unit_type_label = data['请选择贵单位情况']
    unit_mapping = {
        "应急保障类企事业单位": "f0Vp",
        "连续生产/开工类企事业单位": "ffwi",
        "放假后复工（复产）企事业单位": "yhpk"
    }
    unit_value = unit_mapping[unit_type_label]

    radio_button = driver.find_element(By.XPATH,
                                       f"//div[@data-value='{unit_value}']//input[@type='radio'][@value='{unit_value}']")

    radio_button.click()


@when('将第一页进行截图')
def screenshot_first_page(driver):
    driver.save_screenshot("screenshots/page1.png")


@when('点击下一页按钮')
def click_next_page(driver):
    driver.find_element(By.XPATH, '//*[@id="root"]/div/form/div[5]/div[1]/button').click()


@when('点击下一一页按钮')
def click_next_page(driver):
    driver.find_element(By.XPATH, '//*[@id="root"]/div/form/div[4]/div[1]/button[2]').click()


@when(parsers.parse('在第二页填写以下内容:\n{datatable}'))
def fill_second_page(driver, datatable):
    data = parse_datatable(datatable)

    for key in data:
        wait = WebDriverWait(driver, 10)
        input_box = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                           f"//div[contains(text(),'{key}')]/ancestor::div[@class='ant-form-item ant-form-item-with-help sc-fznyAO bYBcZL']//input[@type='text'][@class='ant-input']")))
        input_box.send_keys(data[key])


@when('将第二页进行截图')
def screenshot_second_page(driver):
    driver.save_screenshot("screenshots/page2.png")


@when(parsers.parse('在第三页填写以下内容:\n{datatable}'))
def fill_third_page(driver, datatable):
    data = parse_datatable(datatable)

    input_type = 'input'
    for key in data:
        wait = WebDriverWait(driver, 10)

        if key == '疫情防控方案':
            input_type = 'textarea'

        if key == '复工日期':
            input_box = driver.find_element(By.XPATH,
                                            '//*[@id="root"]/div/form/div[2]/div/div[8]/div/div/div[2]/div[1]/div/div/div/div/span/input')
        else:
            input_box = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                               # f"//div[contains(text(),'{key}')]/ancestor::div[@class='ant-form-item ant-form-item-with-help sc-fznyAO bYBcZL']//input")))
                                                               f"//div[contains(text(),'{key}')]/ancestor::div[contains(@class, 'ant-form-item') and contains(@class, 'ant-form-item-with-help')]//{input_type}")))
        input_box.send_keys(data[key])


@when('将第三页进行截图')
def screenshot_third_page(driver):
    driver.save_screenshot("screenshots/page3.png")


@when('点击提交按钮')
def submit_form(driver):
    submit_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/form/div[4]/div[1]/button[2]')
    submit_button.click()


@then('判断提交成功')
def check_submission_success(driver):
    assert "提交成功" in driver.page_source


@when('将提交结果页进行截图')
def screenshot_result_page(driver):
    driver.save_screenshot("screenshots/result.png")


def parse_datatable(datatable):
    lines = datatable.strip().split('\n')
    result = {}

    for line in lines[1:]:
        key, value = [item.strip() for item in line.split('|')[1:-1]]
        result[key] = value

    return result
