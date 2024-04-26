import base64
import time
import re
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from price_match.models import Product, Config

product_image = None
def scrape_website(url: str) -> Product:
    product = Product()
    product.url = url

    #if not __product_allready_accepted(product.url):
    config = __get_config(product.url)
    page_source, binary_screenshot = scrape_html_from_website(config, product.url)
    get_product_from_html(config, page_source, product, binary_screenshot)
    
    product.save()
    return product


def __product_allready_accepted(url: str)-> bool:
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)

    try:
        Product.objects.get(url=url, creation_datetime__gte=twenty_four_hours_ago)
        return True
    except Product.DoesNotExist:
        return False


def scrape_html_from_website(config: Config, url: str) -> str:
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"

    chrome_options = Options()
    chrome_options.add_argument(f"--user-agent={my_user_agent}")
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1,1")  # Adjust window size here
    url = urlparse(url=url, scheme="https").geturl()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    __prepare_page_for_scraping(config, driver)
    page_source = driver.page_source
    driver.quit()
    binary_screenshot = __take_screenshot(url,driver)
    print(binary_screenshot)
    return page_source, binary_screenshot


def __take_screenshot(url:str, driver:webdriver.Chrome):
    return driver.get_screenshot_as_png()


def __prepare_page_for_scraping(config: Config, driver: webdriver.Chrome) -> None:
    try:
        cookie_selector = config.cookie_selector
        cookie_wait = WebDriverWait(driver, 10)
        cookie_accept = cookie_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"{cookie_selector}")))
        cookie_accept.click()
    except:
        pass # ! Better exception handling

    try:
        slowest_element_selector = config.slowest_element_selector
        slowest_element_wait = WebDriverWait(driver, 10)
        slowest_element_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"{slowest_element_selector}")))
    except:
        pass # ! Better exception handling

    specifications = config.specification_selector.split("¤") # ! Better options?

    for specification in specifications:
        if specification:
            specification_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, specification)))
            for _ in range(3):
                try:
                    specification_element.click()
                    break
                except ElementClickInterceptedException:
                    time.sleep(1)



def get_product_from_html(config: Config, html: str, product: Product, binary_screenshot) -> Product:
    soup = BeautifulSoup(html, "html.parser")

    for field in Product._meta.fields:
        selector = getattr(config, field.name + '_selector', None)

        if selector:
            try:
                value = ""
                if "¤" in selector:
                    selectors = selector.split("¤")
                    for selector in selectors:
                        value += soup.select_one(selector).text
                        value += " "
                else:
                    value = soup.select_one(selector).text

                if field.get_internal_type() == 'FloatField':
                    value = __extract_floats_from_string(value)

                setattr(product, field.name, value)

            except AttributeError:
                setattr(product, field.name, None)
    # product.product_image = binary_screenshot
    # print(binary_screenshot)
    return product


def __get_config(url: str) -> Config:
    no_prefix = url.removeprefix("http://").removeprefix("https://").removeprefix("www.")
    base_url = no_prefix.split("/")[0]
    return Config.objects.get(pk=base_url)


def __extract_floats_from_string(input_string: str) -> float:
    pattern = r"[-+]?\d{1,3}(?:,\d{3})*\.\d+|\d+"
    match = re.search(pattern, input_string)
    if match:
        return float(match.group().replace(',', '')) # ! If no number maybe return whatever string there is?
