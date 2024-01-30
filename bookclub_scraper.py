import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

books = ['lolita', 'the vegetarian', 'roadside picnic']

for book in books:

    # Open driver and search for book
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.goodreads.com')
    search_bar = driver.find_element(By.ID, 'sitesearch_field')
    search_bar.send_keys(book)
    search_bar.send_keys(Keys.RETURN)

    # Close popup
    time.sleep(3)
    popup = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/button')
    popup.click()
    WebDriverWait(driver, 5)

    # Select title and get URL
    title = driver.find_element(By.CLASS_NAME, "bookTitle")
    title.click()
    time.sleep(3)
    get_url = driver.current_url
    print("The current URL is:"+str(get_url))
    driver.quit()