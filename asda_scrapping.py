from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time


def asda_website_rating_scraping(driver):
    soup = BeautifulSoup(driver.page_source, features="lxml")
    item_title = soup.find("h1", class_="pdp-main-details__title")
    item_title = item_title.text
    item_img = soup.find(
        "img", class_="asda-img asda-image asda-image-zoom__small-image"
    )
    item_img = item_img.get("src")
    item_description = soup.find_all(
        "div", class_="pdp-description-reviews__product-details-content"
    )
    item_description = item_description[9].text
    ratings_list = soup.find(
        "div", class_="co-product__rating pdp-main-details__rating"
    )
    if ratings_list:
        ratings_list = ratings_list.get("aria-label")
        ratings_list = ratings_list.split(",")[0]
    # Scroll down by 1000 pixels# Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0,400);")
    time.sleep(5)
    review_tab_buttons = driver.find_elements(By.CLASS_NAME, "asda-tab")
    review_tab_buttons[1].click()
    time.sleep(5)
    return ratings_list, item_title, item_img, item_description


def asda_website_scraping(link):
    rating_function_executed = False
    reviews_list = []
    # Set up Chrome options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Create webdriver object with Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    time.sleep(5)
    cookie_button = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
    cookie_button[0].click()
    if not rating_function_executed:
        ratings_list, item_title, item_img, item_description = (
            asda_website_rating_scraping(driver)
        )
        rating_function_executed = True
    while True:
        try:
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, features="lxml")
            reviews = soup.find_all("p", class_="pdp-description-reviews__content-text")
            reviews_author = soup.find_all(
                "span", class_="pdp-description-reviews__rating-title"
            )
            reviews_author = soup.find_all(
                "span", class_="pdp-description-reviews__rating-title"
            )
            for review, author in zip(reviews, reviews_author):
                reviews_list.append(author.text + " " + review.text)
            disable = soup.find(
                "a",
                class_="asda-btn asda-btn--clear asda-btn--disabled co-pagination__arrow co-pagination__arrow--right co-pagination__arrow--disabled",
            )
            time.sleep(5)
            if not disable:
                next_page_button = driver.find_elements(
                    By.XPATH, "//a[@data-auto-id='btnright']"
                )
                if next_page_button:
                    position = next_page_button[0].location
                    # Scroll to the specific x, y coordinates
                    driver.execute_script(
                        "window.scrollTo(arguments[0], arguments[1]);",
                        position["x"] - 200,
                        position["y"] - 200,
                    )
                time.sleep(5)
                if next_page_button:
                    next_page_button[0].click()
            else:
                break
        except Exception as e:
            print(f"Exception occurred: {e}")
            break
    return reviews_list, ratings_list, item_title, item_img, item_description


reviews_list, ratings_list, item_title, item_img, item_description = (
    asda_website_scraping(
        "https://groceries.asda.com/product/noodle-pots/itsu-katsu-rice-noodles/1000297879129"
    )
)


for i in range(0, len(reviews_list)):
    print("This is review No ", i + 1, "=", reviews_list[i])

print("This here is rating list : ", ratings_list)
print("This here is item list :", item_title)
print(" This here is item img", item_img)
print(" This here is item descrption", item_description)
