import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import io
import os

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

# Reading in Excel sheet

data = pd.read_excel('book_club_books.xlsx').drop(index=0)
data.rename(columns = {'Wishlist': 'Title', 'Unnamed: 1': 'Author'}, inplace=True)
books = data['Title'].tolist()

# Create afolder to store html files

folder = "html_files"
os.makedirs(folder, exist_ok=True)

# Begin scraping goodreads for the page of each book

driver = webdriver.Chrome(options=options)

try: 
    for book in books:

        # Create path
        file_path = os.path.join(folder, f"{book}.html")

        # Open driver and search for book
        driver.get('https://www.goodreads.com')
        search_bar = driver.find_element(By.ID, 'sitesearch_field')
        search_bar.send_keys(book)
        search_bar.send_keys(Keys.RETURN)

        # Check for popup and close it
        try:
            popup = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/button')
            popup.click()
            WebDriverWait(driver, 5)
        except NoSuchElementException:
            pass

        # Select title and get URL
        title = driver.find_element(By.CLASS_NAME, "bookTitle")
        title.click()
        time.sleep(3)
        html = driver.page_source
        time.sleep(1)

        # Prettify html and save it as a file
        soup = BeautifulSoup(html, 'html.parser')
        html = soup.prettify()
        with io.open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

finally:
    driver.quit()
