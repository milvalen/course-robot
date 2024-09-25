import random
import time
import csv
import os

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from multiprocessing import Process
from selenium import webdriver


INITIAL_URL = ''
STOP_URL = ''


def get_profile_path(email: str) -> str:
    base_dir = 'chrome_profiles'
    if not os.path.exists(base_dir): os.makedirs(base_dir)
    return f'{os.getcwd()}/{base_dir}/{email.replace("@", "_at_").replace(".", "_dot_")}'


def click_next_page(driver: WebDriver, button: WebElement):
    ActionChains(driver).move_to_element(button).click().perform()


def process_video(driver: WebDriver, email: str, video: WebElement):
    video_duration = driver.execute_script('return arguments[0].duration;', video)
    wait_time = max(video_duration + random.randint(10, 30), 300)

    print(f'{email}: Video detected with duration {video_duration} seconds, waiting for {wait_time} seconds.')
    time.sleep(wait_time)

def process_empty(email: str):
    wait_time = random.randint(300, 360)
    print(f'{email}: No PDF or video detected, waiting for {wait_time} seconds.')
    time.sleep(wait_time)

def process_material(driver: WebDriver, email: str):
    try:
        time.sleep(10)
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
        time.sleep(1)

        button_elements = driver.find_elements(
            By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/button[2]'
        )
        
        header_elements = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/h1')
        pdf_elements = driver.find_elements(By.CLASS_NAME, 'react-pdf__Document')
        nested_iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        video_elements = driver.find_elements(By.TAG_NAME, 'video')

        if header_elements: print(f'\n{email}: {header_elements[0].get_attribute("innerText")}')
        else: raise Exception(f'{email}: No header element')
        
        if pdf_elements:
            page_count = len(pdf_elements[0].find_elements(By.XPATH, './div'))
            wait_time = max(page_count * 30, 300)

            print(f'{email}: PDF detected with {page_count} pages, waiting for {wait_time} seconds.')
            time.sleep(wait_time)
        elif video_elements:
            process_video(driver, email, video_elements[0])
        elif nested_iframes:
            driver.switch_to.frame(nested_iframes[0])
            time.sleep(1)
            video_elements = driver.find_elements(By.TAG_NAME, 'video')
            
            if video_elements: process_video(driver, email, video_elements[0])
            else: process_empty(email)

            driver.switch_to.default_content()
            time.sleep(1)
            driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
            time.sleep(1)
        else: process_empty(email)

        if button_elements: click_next_page(driver, button_elements[0])
        else: raise Exception(f'{email}: No button element')

        driver.switch_to.default_content()
        time.sleep(1)
    except Exception as e:
        driver.refresh()
        print(f'{email}: {str(e).split(chr(10))[0]}, refreshing...')
        time.sleep(10)


def run_for_account(email: str, password: str):
    chrome_options = Options()

    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument(f'user-data-dir={get_profile_path(email)}')
    chrome_options.add_argument('--headless=old')
    chrome_options.add_argument('--log-level=3')

    driver = webdriver.Chrome(chrome_options)
    print(f'{email} loaded')

    driver.get(INITIAL_URL)
    time.sleep(3)
    
    if 'login' in driver.current_url:
        input_elements = driver.find_elements(By.TAG_NAME, 'input')
        input_elements[0].send_keys(email)
        input_elements[2].send_keys(password)
        driver.find_elements(By.TAG_NAME, 'button')[1].click()

        print(f'{email} logged in')

        time.sleep(10)
        driver.find_elements(By.TAG_NAME, 'button')[1].click()

        print(f'{email} authorized')
    elif 'authorize' in driver.current_url:
        driver.find_elements(By.TAG_NAME, 'button')[1].click()
        print(f'{email} authorized')
    
    if driver.find_elements(By.CLASS_NAME, 'app-captcha'):
        print(f'\n{email}: captcha found! try another time...\n')
        os._exit(1)

    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/span'):
        print(f'{email} got authorization error, reloading...')

        driver.close()
        run_for_account(email, password)
    else:
        print(f'{email} started')
        while driver.current_url != STOP_URL: process_material(driver, email)
        print(f'\n{email} finished!')


if __name__ == '__main__':
    with open('accounts.csv', newline='') as csvfile:
        for row in csv.reader(csvfile): 
            Process(target=run_for_account, args=(row[0], row[1])).start()