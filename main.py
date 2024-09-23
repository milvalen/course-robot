import random
import time
import csv
import os

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from multiprocessing import Process
from selenium import webdriver

INITIAL_URL = 'https://edubasmik.lms.2035.university/viewer/sessions/217/materials/3467'


def get_profile_path(email):
    base_dir = 'chrome_profiles'
    if not os.path.exists(base_dir): os.makedirs(base_dir)
    return os.path.join(base_dir, email.replace('@', '_at_').replace('.', '_dot_'))


def click_next_page(driver):
    button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/button[2]')

    ActionChains(driver).move_to_element(button).click().perform()
    print(button)


def process_material(driver, email):
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))

    pdf_elements = driver.find_elements(By.CLASS_NAME, 'react-pdf__Document')
    video_elements = driver.find_elements(By.TAG_NAME, 'video')

    if pdf_elements:
        page_count = len(pdf_elements[0].find_elements(By.TAG_NAME, 'div'))
        wait_time = max(page_count * 30, 300)
        print(f'{email}: PDF detected with {page_count} pages, waiting for {wait_time} seconds.')

        time.sleep(wait_time)
    elif video_elements:
        video = video_elements[0]
        video_duration = driver.execute_script('return arguments[0].duration;', video)
        wait_time = max(video_duration + random.randint(10, 30), 300)
        print(f'{email}: Video detected with duration {video_duration} seconds, waiting for {wait_time} seconds.')

        time.sleep(wait_time)
    else:
        wait_time = random.randint(300, 360)
        print(f'{email}: No PDF or video detected, waiting for {wait_time} seconds.')

        time.sleep(wait_time)

    click_next_page(driver)
    driver.switch_to.default_content()


def run_for_account(email, password):
    chrome_options = Options()

    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument(f'user-data-dir={get_profile_path(email)}')
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(INITIAL_URL)
    time.sleep(3)

    if "login" in driver.current_url:
        input_elements = driver.find_elements(By.TAG_NAME, 'input')

        input_elements[0].send_keys(email)
        input_elements[2].send_keys(password)
        driver.find_elements(By.TAG_NAME, 'button')[1].click()
        time.sleep(10)
        driver.find_elements(By.TAG_NAME, 'button')[1].click()
    elif "authorize" in driver.current_url:
        driver.find_elements(By.TAG_NAME, 'button')[1].click()

    time.sleep(30)

    while True: process_material(driver, email)


if __name__ == '__main__':
    with open('accounts.csv', newline='') as csvfile:
        for row in csv.reader(csvfile):
            Process(target=run_for_account, args=(row[0], row[1])).start()
