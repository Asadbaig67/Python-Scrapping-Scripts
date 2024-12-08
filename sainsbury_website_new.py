from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time


def Sainsbury_website_rating_scraping(driver):
    soup = BeautifulSoup(driver.page_source, features="lxml")
    item_title = soup.find("h1", class_="pd__header")
    item_title = item_title.text
    item_img = soup.find("img", class_="pd_image pdimage_nocursor")
    print(item_img)
    # item_img = item_img.get("src")
    rating = soup.find("div", class_="ds-c-rating__stars")
    rating = rating.get("aria-label")
    item_description = soup.find_all("div", class_="itemTypeGroupContainer productText")
    print(item_description)
    # item_description = item_description[0].text
    time.sleep(5)
    review_tab_buttons = driver.find_element(By.ID, "tab-reviews")
    review_tab_buttons.click()
    time.sleep(5)
    return rating, item_title, item_img, item_description


def Sainsbury_website_scraping(link):
    rating_function_executed = False
    reviews_list = []
    ratings = []
    # Set up Chrome options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    )
    # Create webdriver object with Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    time.sleep(5)
    cookie_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    cookie_button.click()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, features="lxml")
    if not rating_function_executed:
        ratings, item_title, item_img, item_description = (
            Sainsbury_website_rating_scraping(driver)
        )
        rating_function_executed = True
    while True:
        try:
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, features="lxml")
            authors = soup.find_all("div", class_="review__author")
            reviews = soup.find_all("div", class_="review__title")
            reviews_extension = soup.find_all("div", class_="review__content")
            for review, author, review_extended in zip(
                reviews, authors, reviews_extension
            ):
                author_tag = review.find_previous("div", class_="review__author")
                author_name = author_tag.text if author_tag else "Anonymous"
                reviews_list.append(
                    author_name + " --> " + review.text + " " + review_extended.text
                )
            time.sleep(5)
            # Assuming 'driver' is your WebDriver instance
            next_page_button = driver.find_elements(
                By.XPATH, "//a[@aria-label='Next page']"
            )
            driver.implicitly_wait(5)
            if next_page_button:
                next_page_button[0].click()
            else:
                break
        except Exception as e:
            print(f"Exception occurred: {e}")
            break
    return reviews_list, ratings, item_title, item_img, item_description


Sainsbury_reviews, Sainsbury_ratings, item_title, item_img, item_description = (
    Sainsbury_website_scraping(
        "https://www.sainsburys.co.uk/gol-ui/product/itsu-vegetable-fusion-gyoza-dinner-dumplings-x20-300g"
    )
)

print(Sainsbury_reviews)
print(Sainsbury_ratings)
print(item_title)
print(item_img)
print(item_description)
