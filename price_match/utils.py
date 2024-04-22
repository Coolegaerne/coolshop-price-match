import json
from price_match.models import Product, Config

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
import re
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse


def with_product(url:str):
    product = Product()
    product.url = url
    scrape_website(product)


def scrape_website(product: Product) -> Product:
    config = __get_config(product.url)

    page_source = scrape_html_from_website(config, product.url)
    return get_product_from_html(config, page_source, product)


def scrape_html_from_website(config: Config, url: str) -> str:
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"

    chrome_options = Options()
    chrome_options.add_argument(f"--user-agent={my_user_agent}")
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--disable-gpu')
    url = urlparse(url=url, scheme="https").geturl()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    try:
        cookie_selector = config.cookie_selector
        cookie_wait = WebDriverWait(driver, 10)
        cookie_accept = cookie_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"{cookie_selector}")))
        cookie_accept.click()
    except:
        pass
    
    slowest_element_selector = config.slowest_element_selector
    slowest_element_wait = WebDriverWait(driver, 10)
    slowest_element_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"{slowest_element_selector}")))
    
    specifications = config.specification_selector.split("¤")
    
    for specification in specifications:
        if specification:
            print(specification)
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


def get_product_from_html(config: Config, html: str, product: Product) -> Product:
    soup = BeautifulSoup(html, "html.parser")
    try:
        str_price = soup.select_one(config.price_selector).text
        product.price = __extract_floats_from_string(str_price)
    except:
        pass
    try:
        product.name = soup.select_one(config.name_selector).text
    except:
        pass
    try:
        
        product.ean = soup.select_one(config.ean_selector).text
    except:
        pass
    try:
        product.color = soup.select_one(config.color_selector).text
    except:
        pass
            
    try:
        product.in_stock = soup.select_one(config.stock_status_selector).text
    except:
        pass
        
    try:
        str_shipping_price = soup.select_one(config.shipping_price_selector).text
        product.shipping_cost = __extract_floats_from_string(str_shipping_price)
    except:
        pass

    print(product)
    return product


def __get_config(url: str) -> Config:
    no_prefix = url.removeprefix("http://").removeprefix("https://").removeprefix("www.")
    base_url = no_prefix.split("/")[0]
    return Config.objects.get(pk=base_url)


def __extract_floats_from_string(input_string):
        pattern = r"[-+]?\d{1,3}(?:,\d{3})*\.\d+|\d+"
        match = re.search(pattern, input_string)
        if match:
            return float(match.group().replace(',', ''))
        