from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def Holland_Barrett_website_rating_scraping(driver):
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, features="lxml")
    item_title = soup.find("h1", class_="ProductHeaderUI-module_title__Snpxr")
    item_title = item_title.text
    item_img = soup.find("img", class_="DesktopZoomImage-module_image__AHQyj")
    item_img = item_img.get("src")
    ratings = soup.find("p", class_="ReviewsSection-module_reviewScore__-5nU9")
    ratings = ratings.text
    description_button = driver.find_elements(
        By.CLASS_NAME, "Accordion-module_trigger__t713I"
    )
    description_button[0].click()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, features="lxml")
    item_description = soup.find("div", class_="Accordion-module_content__Sb0zM")
    item_description = item_description.text
    return ratings, item_title, item_img, item_description


def Holland_Barrett_website_scraping(link):
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

    # driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(5)
    cookie_button = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
    cookie_button[0].click()
    if not rating_function_executed:
        ratings, item_title, item_img, item_description = (
            Holland_Barrett_website_rating_scraping(driver)
        )
        rating_function_executed = True
    while True:
        try:
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, features="lxml")
            authors = soup.find_all("p", class_="ReviewItem-module_username__-vsS8")
            reviews = soup.find_all("p", class_="ReviewItem-module_title__mpu4W")
            reviews_second_part = soup.find_all(
                "p", class_="ReviewItem-module_text__rUxPq"
            )
            for review, review_part_2, author in zip(
                reviews, reviews_second_part, authors
            ):
                reviews_list.append(
                    author.text + " " + review.text + " " + review_part_2.text
                )
            time.sleep(5)
            # Assuming 'driver' is your WebDriver instance
            next_page_button = driver.find_elements(
                By.XPATH,
                "//button[@class='Pagination-module_button__7gJRV' and @title='Next']",
            )
            if next_page_button:
                next_page_button[0].click()
            else:
                break
        except Exception as e:
            print(f"Exception occurred: {e}")
            break

    return reviews_list, ratings, item_title, item_img, item_description


reviews_list, ratings_list, item_title, item_img, item_description = (
    Holland_Barrett_website_scraping(
        "https://www.hollandandbarrett.com/shop/product/itsu-sea-salt-crispy-seaweed-thins-5g-6100003896"
    )
)


for i in range(0, len(reviews_list)):
    print("This is review No ", i + 1, "=", reviews_list[i])

print("This here is rating list : ", ratings_list)
print("This here is item list :", item_title)
print(" This here is item img", item_img)
print(" This here is item descrption", item_description)
