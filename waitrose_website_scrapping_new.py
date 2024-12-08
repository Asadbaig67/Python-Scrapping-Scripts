from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def waitrose_and_partners_website_rating_scraping(driver):
    ratings = []
    soup = BeautifulSoup(driver.page_source, features="lxml")
    item_title = soup.find("span", class_="ProductHeader_name__ABMK2")
    item_title = item_title.text
    # item_title_extended_part = soup.find(
    #     "span", class_="ProductSize_size_3kv3Y ProductHeader_sizeMessage_e9XyK"
    # )
    # item_title_extended_part = item_title_extended_part.text
    # item_title = item_title + " " + item_title_extended_part
    item_img = soup.find("div", class_="ProductImage_detailsContainer__hY1qi")
    item_img = item_img.img.get("src")
    rating = soup.find_all("div", class_="bv-inline-histogram-ratings-score")
    for rate in rating:
        ratings.append(rate.span.text)
    item_description = soup.find_all(
        "section", class_="ProductDescriptions_description_4DWA"
    )
    print("This is item description : ", item_description)
    if len(item_description) > 1:
        item_description = item_description[0].text + item_description[1].text
    return ratings, item_title, item_img, item_description


def waitrose_and_partners_website_scraping(link):
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
    cookie_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "CookieConsent_acceptAll__U3u_s")
        )
    )
    cookie_button.click()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, features="lxml")
    rate_button = soup.find("a", class_="btn no")
    if rate_button:
        rate_button.click()
    else:
        if not rating_function_executed:
            ratings, item_title, item_img, item_description = (
                waitrose_and_partners_website_rating_scraping(driver)
            )
            rating_function_executed = True
        while True:
            try:
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, features="lxml")
                authors = soup.find_all(
                    "button",
                    class_="bv-author bv-fullprofile-popup-target bv-focusable",
                )
                reviews = soup.find_all("div", class_="bv-content-summary-body-text")
                for review, author in zip(reviews, authors):
                    author_tag = review.find_previous(
                        "button",
                        class_="bv-author bv-fullprofile-popup-target bv-focusable",
                    )
                    author_name = author_tag.h3.text if author_tag else "Anonymous"
                    reviews_list.append(author_name + " --> " + review.text)
                time.sleep(5)
                # Assuming 'driver' is your WebDriver instance
                next_page_button = driver.find_elements(
                    By.XPATH, "//a[contains(@class, 'bv-content-btn-pages-last')]"
                )
                if next_page_button:
                    next_page_button[0].click()
                else:
                    break
            except Exception as e:
                print(f"Exception occurred: {e}")
                break
    return reviews_list, ratings, item_title, item_img, item_description


(
    waitrose_and_partners_reviews,
    waitrose_and_partners_ratings,
    item_title,
    item_img,
    item_description,
) = waitrose_and_partners_website_scraping(
    "https://www.waitrose.com/ecom/products/waitrose-cooked-smokey-chipotle-lime-chicken-pieces/537823-824560-824561"
)


print(waitrose_and_partners_reviews)
print(waitrose_and_partners_ratings)
print("This is Name : ", item_title)
print(item_img)
print(item_description)
