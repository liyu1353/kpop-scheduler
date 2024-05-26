from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import pygsheets
import pandas as pd


def classify(title):
    if "release announcement" in title.capitalize():
        return "Release"
    if "tour" in title.capitalize():
        return "Tour"
    if "fansign" in title.capitalize():
        return "Fansign"
    if "participate" in title.capitalize():
        return "Music Show"
    if "awards" in title.capitalize():
        return "Award Show"
    return "None"

def findyear(words):
    if "2023" in words:
        return "2023"
    elif "2023." in words:
        return "2023."
    elif "2024" in words:
        return "2024"
    elif "2024." in words:
        return "2024."
    else:
        return None

#for finding dates when it's most likely to appear first
def finddate(text):
    words = text.split(" ")
    year = findyear(words)
    if year is None:
        return None
    while not words[words.index(year) - 1][0: len(words[words.index(year)-1]) - 1].isnumeric():
        words = words[words.index(year) + 1:]
        year = findyear(words)
        if year is None:
            return None
    a = words.index(year)
    if year.isnumeric():
        return words[a - 2] + " " + words[a - 1] + " " + words[a]
    else:
        return words[a - 2] + " " + words[a - 1] + " " + words[a][0, 3]

def getregion(text):
    regioncount = 0
    region = "Korea"
    if "니" in text[:150] or "korea" in text.lower():
        regioncount += 1
        return region
    elif "united states" in text.lower():
        regioncount += 1
        region = "US"
    elif "ま" in text[:150] or "japan" in text.lower():
        regioncount += 1
        region = "Japan"
    else:
        region = "International"
    if regioncount > 1:
        return "International"
    else:
        return region

def description(title):
    if title.lower()[:8] == "[notice]":
        return title[8:]
    elif title[:4] == "[공지]":
        return title[4:]
    else:
        return title[6:]

def txt(driver):
    # the events are all class = NoticeListView_notice_item__1-Ud8
    WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'NoticeListView_notice_item_link__uBuv-')))

    notices = driver.find_elements(By.CLASS_NAME, 'NoticeListView_notice_item_link__uBuv-')

    gc = pygsheets.authorize(service_file='/Users/daniel/PycharmProjects/scheduler/creds/scheduler-409417-e731d6b458a7.json')
    df = pd.DataFrame()
    sh = gc.open('Scheduler Database')
    currSheet = sh[0]

    for notice in notices:
        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, 'NoticeListView_notice_item_link__uBuv-')))
        link = notice.get_attribute("href")
        current = driver.current_window_handle
        script = "window.open('" + link + "')"
        driver.execute_script(script)
        new_tab = [tab for tab in driver.window_handles if tab != current][1]
        driver.switch_to.window(new_tab)
        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, 'p')))
        text = driver.find_element(By.CLASS_NAME, 'p').text
        title = driver.find_element(By.CLASS_NAME, 'NoticeModalView_title__512XG').text
        category = classify(title)
        region = getregion(text)
        desc = description(title)
        if not finddate(text) is None:
            date = finddate(text)
            values_list = ['TXT', date, category, region, desc]
            currSheet.insert_rows(row=2, number=1, values=values_list)
            currSheet.sort_range("A2", "E1000", basecolumnindex=1, sortorder='DESCENDING')

        driver.close()
        driver.switch_to.window(current)
