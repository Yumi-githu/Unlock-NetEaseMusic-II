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
    browser.add_cookie({"name": "MUSIC_U", "value": "006DC6253808F7A3770E929EE2E40B46038559E7589581D859E3869443F74096926B98894BD448234B620FD02B060C1597E5E909703910CDBC9021E214F1692C232235DF0AB10418BD6B5910EA13C09FE25D890F3B12CCD334AACF37BE8913EB5B9EA96924F7787C006C31DAF0847A00D376127CBC08A8FA702EF2616A78AF30FCB13435657A7A63DB8165A338286CD0CF0205365C07931F97B5F2EFC87C537F35CEFD00EF0F940AFE73076A76C0A60F181B60283E89DC7CE1A83C0AD4840086E912F683D40828EB0443B8FC09DA3ABE3A04143A2DBE049B190FABE17F1D8226B45B1D3278DC87CD99E710AFDBEDF9CBC44F3DB110C3ACAEE231C18345EA8401B853BC485D8C1708C9441AA8ADB3CC82BC7D06C415ECABEDEFF27BF415D8797189410311DDBC96032DD32E79AB9F97BCE639E9466E28F0C379AE419DB0F2AC996A48D1A0C691BDBB175616246A21424918A515D1D8EFD50E2775E1A99A8FA2C05E"})
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
