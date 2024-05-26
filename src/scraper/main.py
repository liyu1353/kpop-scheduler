import enha
import txt
import newjeans
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


import time
import pygsheets
import pandas as pd

#try headless?
options = Options()
options.add_argument("--headless=new")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
driver = webdriver.Chrome(options=options)


def login():
    WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located((By.NAME, 'userEmail'))).send_keys("daniel.li7691@gmail.com")

    email_submit = WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="sc-763a3587-1 gOzeoU"]')))

    driver.execute_script("arguments[0].style.zIndex = '9999';", email_submit)
    email_submit.click()

    password = WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located((By.NAME, 'password'))).send_keys("Daniel2005!")

    pass_submit = WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="sc-763a3587-1 gOzeoU"]')))
    driver.execute_script("arguments[0].style.zIndex = '9999';", pass_submit)
    pass_submit.click()


driver.get("https://account.weverse.io/en/signup?authType=redirect&client_id=weverse&redirect_uri=https%3A%2F%2Fweverse.io%2FloginResult%3Ftopath%3D%252F&user_device_id=961d7fcc-f4cb-4d98-8fda-479289160330")

login()

WebDriverWait(driver, 1000)

#switch to enhypen tab
homepage = driver.current_window_handle
script = "window.open('https://weverse.io/enhypen/notice')"
driver.execute_script(script)
new_tab = [tab for tab in driver.window_handles if tab != homepage][0]
driver.switch_to.window(new_tab)
driver.refresh()
enha.enhypen(driver)
driver.close()
driver.switch_to.window(homepage)

#switch to txt tab
script = "window.open('https://weverse.io/txt/notice')"
driver.execute_script(script)
new_tab = [tab for tab in driver.window_handles if tab != homepage][0]
driver.switch_to.window(new_tab)
driver.refresh()
txt.txt(driver)
driver.close()
driver.switch_to.window(homepage)

#switch to newjeans tab
script = "window.open('https://weverse.io/newjeansofficial/notice')"
driver.execute_script(script)
new_tab = [tab for tab in driver.window_handles if tab != homepage][0]
driver.switch_to.window(new_tab)
driver.refresh()
newjeans.newjeans(driver)
driver.close()
