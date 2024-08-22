from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import datetime
import os
import platform

INITIAL_URL = 'https://edubas.lms.2035.university/viewer/sessions/213/materials/3211'
EMAIL = ''
PASSWORD = ''


def advance_time_by_five_minutes():
    new_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
    os.system(f'time {new_time.strftime('%H:%M:%S')}'
              if platform.system() == 'Windows' 
              else f'date {new_time.strftime('%m%d%H%M%Y.%S')}')


def click_next_page():
    body_element = driver.find_element(By.TAG_NAME, 'body')
    body_width = driver.get_window_size()['width']
    body_height = driver.get_window_size()['height']
    click_x = body_width / 4 + 150
    click_y = body_height / 4 + 100
    ActionChains(driver).move_to_element_with_offset(body_element, click_x, click_y).click().perform()


def process_material():
    advance_time_by_five_minutes()
    time.sleep(21)
    click_next_page()
    time.sleep(3)


if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(INITIAL_URL)
    time.sleep(3)
    driver.find_elements(By.TAG_NAME, 'input')[0].send_keys(EMAIL)
    driver.find_elements(By.TAG_NAME, 'input')[2].send_keys(PASSWORD)
    driver.find_elements(By.TAG_NAME, 'button')[1].click()
    time.sleep(50)

    while True:
        process_material()
