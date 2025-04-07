# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0096563E7A2E2C0B9FB391545F0B0C6E72DC6172565972C16725FA28F3002EA4C5C3A96289BDAA8F20EBFC886AA52DC17A2BFBD040ACF769469B7DD558D80A613530D3E1F887F6DF1ED1C5D572400CE7DDCE2095FE558712D2E4BCB51DAA47FE80468BD103D899404F9981222A6E830BDE9B2AB1A89C7939B5DF9B93F8F2E9FB5D7BDD37C5901FDBFF33616242738039D5A64BC983CDA96488B0AA865468E18CD5194B373EA4C692CAAC6BB24DD1024F766D7D3DC67947C86B1889F7859949E099FD38A213DEF1C709A4C262E62C0D0B9B72948A83EACE70A47D5F29A39D57D840E974F6411D846F62563F4661EF6566DB5A3A55C61C64C6FFEA5BC948FDE11B9F408CE2C522474581341C13A2CE657D560A2E22687BB99B4EC3829259BBE7EFC343BBC42AABCF0DD566A4C04575322945AE2337528147B8CB825DAAEE229BAA4A23AF3D5B66D394FE0495237D694DE3F5FC95A8CF6ED7E00F79E00CCC9117A100"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
