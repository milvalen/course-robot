from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
import os

INITIAL_URL = ''
EMAIL = ''
PASSWORD = ''


def get_profile_path(email):
    base_dir = 'chrome_profiles'

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    return os.path.join(base_dir, email.replace('@', '_at_').replace('.', '_dot_'))


def click_next_page():
    button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/button[2]')
    ActionChains(driver).move_to_element(button).click().perform()
    print(button)


#TODO: research content attributes
def process_material():
    driver.switch_to.frame(driver.find_element(By.ID, 'materialFrame'))
    
    if driver.find_elements(By.TAG_NAME, 'embed'): # research pdf tag
        try:
            page_count = int(driver.find_element(By.CLASS_NAME, 'page-count').text) # research pdf page-count
        except:
            page_count = 1
        
        wait_time = max(page_count * 30, 300)
        print(f'PDF detected with {page_count} pages, waiting for {wait_time} seconds.')
        time.sleep(wait_time)
    
    video_elements = driver.find_elements(By.TAG_NAME, 'video')
    
    if video_elements:
        video = video_elements[0]
        driver.execute_script('arguments[0].play();', video)
        video_duration = driver.execute_script('return arguments[0].duration;', video)
        wait_time = max(video_duration + random.randint(10, 30), 300)
        print(f'Video detected with duration {video_duration} seconds, waiting for {wait_time} seconds.')
        time.sleep(wait_time)
    else:
        wait_time = random.randint(300, 360)
        print(f'No PDF or video detected, waiting for {wait_time} seconds.')
        time.sleep(wait_time)

    click_next_page()
    driver.switch_to.default_content()


if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument(f'user-data-dir={get_profile_path(EMAIL)}')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(INITIAL_URL)
    time.sleep(3)

    if "login" in driver.current_url:
        driver.find_elements(By.TAG_NAME, 'input')[0].send_keys(EMAIL)
        driver.find_elements(By.TAG_NAME, 'input')[2].send_keys(PASSWORD)
        driver.find_elements(By.TAG_NAME, 'button')[1].click()
    time.sleep(50)
    
    while True:
        process_material()
