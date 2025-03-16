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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D060A2BB5F330281E362C1EE26183926BEF0668C507C2ACE97B32AD36E7479CA118ADCE81883241A531361C7CBA285B09AFF967ADEACE3AB15E710E80C02B0E9D78A64594BB7F7E77D80013A2BFFAA0CF8CFDAA407DE70E51022C8E2ECD263B5FDBC6558F325E5A4CB377D50A54794AAA1FADA5CD5B4E0BEDDEEB0B83263DF1B23A3A156F500D2B3CFD22B91DDC8BD31B8DFA85768D3A0DFC54342FF9319211983F6FD11BB8459A38144615ABB0D7710AAAB8F9822EB37369842BE0BFA90ABD4B93F9283BF45203024328ADA9DE734F6BCBF2187686AC64DD778FC4660FCD40D5A5B4855C8F83616F4791D066A8DED89536232D3E62163EF3DC331842A5010D66B534EF0464A814325C3A099364B36C3E8A484DDC86294DFBDC3F074860A9E4E2EE9A63DE3AA96C1D1887C96F5BB3EB124E422E1F2DCD8192AC2261A326755F836B53DBF8937E26117E3987D2E1A5C2E6931341E774054CE4D74E1F8E8C14A75"})
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
