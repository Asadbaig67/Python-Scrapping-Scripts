from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time


def tesco_website_rating_scraping(driver):
    
    soup = BeautifulSoup(driver.page_source, features="lxml")
    item_title = soup.find(
        "h1",
        class_="component__StyledHeading-sc-1t0ixqu-0 kdSqXr ddsweb-heading styled__ProductTitle-mfe-pdp__sc-ebmhjv-6 flNJKr",
    )
    print(item_title)
    item_title = item_title.text
    item_img = soup.find(
        "img", class_="styled__Image-sc-j2gwt2-0 llJlgM ddsweb-responsive-image__image"
    )
    item_img = item_img.get("src")
    print(item_img)
    rating = soup.find("span", class_="ddsweb-star-rating__average-rating-text")
    rating = rating.text + " out of 5"
    item_description = soup.find_all(
        "span", class_="styled__Block-mfe-pdp__sc-1od89q4-1 bICtby"
    )
    item_description = "".join(element.text for element in item_description[:9])
    driver.execute_script("window.scrollTo(0,3000);")
    return rating, item_title, item_img, item_description


def tesco_website_scraping(link):
    rating_function_executed = False
    reviews_list = []
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
    soup = BeautifulSoup(driver.page_source, features="lxml")
    if not rating_function_executed:
        ratings, item_title, item_img, item_description = tesco_website_rating_scraping(
            driver
        )
        rating_function_executed = True
    while True:
        try:
            time.sleep(5)
            next_page_button = driver.find_elements(
                By.XPATH,
                "//button[@type='button' and contains(@class, 'styled__StyledTextButton-sc-8hxn3m-0')]",
            )
            driver.implicitly_wait(15)
            if next_page_button:
                time.sleep(5)
                next_page_button[0].click()
            else:
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, features="lxml")
                reviews = soup.find_all(
                    "span",
                    class_="text__StyledText-sc-1jpzi8m-0 iksSWU ddsweb-text styled__Content-mfe-pdp__sc-je4k7f-6 vnTTI",
                )
                reviews_extension = soup.find_all(
                    "span",
                    class_="text__StyledText-sc-1jpzi8m-0 eifUHO ddsweb-text styled__ReviewDate-mfe-pdp__sc-je4k7f-9 dMiXWb",
                )
                for review, review_extended in zip(reviews, reviews_extension):
                    reviews_list.append(review_extended.text + " --> " + review.text)
                break
        except Exception as e:
            print(f"Exception occurred: {e}")
            break
    return reviews_list, ratings, item_title, item_img, item_description


tesco_reviews, tesco_ratings, item_title, item_img, item_description = (
    tesco_website_scraping("https://www.tesco.com/groceries/en-GB/products/312708988")
)


# Print the results in formmated way
print(f"Item Title: {item_title}")
print(f"Item Image: {item_img}")
print(f"Item Description: {item_description}")
print(f"Item Rating: {tesco_ratings}")
print("Reviews:")
for review in tesco_reviews:
    print(review)
