from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random

INITIAL_URL = 'https://edubas.lms.2035.university/viewer/sessions/213/materials/3211'
EMAIL = '9207457@mail.ru'
PASSWORD = 'Timon05022007'


def click_next_page():
    driver.switch_to.frame(driver.find_element(By.ID, "materialFrame"))
    button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/button[2]')
    print(button)
    ActionChains(driver).move_to_element(button).click().perform()


def process_material():
    time.sleep(random.randint(300, 360))
    click_next_page()


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
