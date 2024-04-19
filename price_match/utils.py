import json
from price_match.models import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException
import time
from PIL import Image
import io
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse


def with_product(url:str):
    product = Product()
    product.url = url
    scrape_website(product)


def scrape_website(product: Product) -> Product:
    config_file = __get_config_file(product.url)

    page_source = scrape_html_from_website(config_file, product.url)
    return get_product_from_html(config_file, page_source, product)


def scrape_html_from_website(config_file: dict, url: str) -> str:
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"

    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument(f"--user-agent={my_user_agent}")
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--disable-gpu')
    url = urlparse(url=url, scheme="https").geturl()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    try:
        cookie_selector = config_file.get("cookie_selector")
        cookie_wait = WebDriverWait(driver, 10)
        cookie_accept = cookie_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"{cookie_selector}")))
        cookie_accept.click()
    except:
        pass

    slowest_element_selector = config_file.get("slowest_element_selector")
    slowest_element_wait = WebDriverWait(driver, 10)
    slowest_element_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"{slowest_element_selector}")))
    
    specifications = config_file.get("specification_selector")
    if specifications:
        for specification in specifications:
            specification_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, specification)))
            for _ in range(3):
                try:
                    specification_element.click()
                    break
                except ElementClickInterceptedException:
                    time.sleep(1)
    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    # image_data = driver.get_screenshot_as_png()
    # image = Image.open(io.BytesIO(image_data))
    # # Display the image
    # image.show()
    
    page_source = driver.page_source
    driver.quit()

    return page_source


def get_product_from_html(config_file: dict, html: str, product: Product) -> Product:
    soup = BeautifulSoup(html, "html.parser")
    value_dict = {}
    config_keys = list(config_file.keys())[3:]
    for key in config_keys:
        value = config_file.get(key)
        try:
            value = soup.select_one(value).get_text()
            value_dict[key] = value
        except:
            pass
    product.create_from_dict(value_dict)
    print(product)
    return product

def __get_config_file(url: str) -> dict:
    no_prefix = url.removeprefix("http://").removeprefix("https://").removeprefix("www.")
    base_url = no_prefix.split("/")[0]
    file_path = f"price_match/website_configs/{base_url}.json"
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Config file for {base_url} not found.")
        return None
