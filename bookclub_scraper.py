import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import os

# Initializing some web driver options

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

# Reading in Excel sheet

data = pd.read_excel('book_club_books.xlsx').drop(index=0)
books = data['Title'].tolist()

# Create a folder to store reviews

output_folder = "reviews"
os.makedirs(output_folder, exist_ok=True)

# Begin scraping goodreads for each book

driver = webdriver.Chrome(options=options)

try: 
    for book in books:

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

        # Select title and get source information
        title = driver.find_element(By.CLASS_NAME, "bookTitle")
        title.click()
        WebDriverWait(driver, 5)
        html = driver.page_source
        WebDriverWait(driver, 5)

        # Pass source information to Parser and prettify it
        prettified_html = BeautifulSoup(html, 'html.parser').prettify()
        soup = BeautifulSoup(prettified_html, 'html.parser')

        # Find reviews and set up path to store them
        review_sections = soup.find_all('section', class_='ReviewText')
        file_path = os.path.join(output_folder, f"{book} reviews.xlsx")
        reviews_list = []

        # Iterate through each review section
        for index, section in enumerate(review_sections, 1):
            
            # Get the text content, removing HTML tags
            cleaned_text = section.get_text(separator=' ', strip=True)
            
            # Append the cleaned text to the list
            reviews_list.append({'Review Number': index, 'Review Text': cleaned_text})

        # Create a DataFrame from the list of reviews
        reviews_df = pd.DataFrame(reviews_list)

        excel_sheet = reviews_df.to_excel(file_path, index=False)

        # Display the Excel file path
        print(f'{book} Reviews DataFrame has been exported to: {output_folder}')

except Exception as e:
        print(f"Error processing {book}: {str(e)}")

finally:
    driver.quit()