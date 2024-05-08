import re
import time
from datetime import timedelta
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django.utils import timezone
from price_match.models import Config, PriceMatch, StatusMessages
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def scrape_website(url: str, postal_code: str, email: str) -> StatusMessages:
    price_match = PriceMatch()
    price_match.url = url
    price_match.postal_code = postal_code
    price_match.email = email
    if __product_already_accepted(price_match.url):
        return StatusMessages.ALREADY_EXIST
    else:
        config = __get_config(price_match.url)
        page_source, binary_screenshot = scrape_html_from_website(
            config, price_match.url
        )
        get_product_from_html(config, page_source, price_match, binary_screenshot)
        price_match.save()
        return StatusMessages.SUCCESS


def __product_already_accepted(url: str) -> bool:
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
    return PriceMatch.objects.filter(
        url=url, creation_datetime__gte=twenty_four_hours_ago
    ).exists()


def scrape_html_from_website(config: Config, url: str) -> str:
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"

    chrome_options = Options()
    chrome_options.add_argument(f"--user-agent={my_user_agent}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1500,6000")
    url = urlparse(url=url, scheme="https").geturl()
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url)
    __prepare_page_for_scraping(config, driver)
    page_source = driver.page_source
    binary_screenshot = __take_screenshot(url, driver)

    driver.quit()
    return page_source, binary_screenshot


def __take_screenshot(url: str, driver: webdriver.Chrome):
    return driver.get_screenshot_as_png()


def __prepare_page_for_scraping(config: Config, driver: webdriver.Chrome) -> None:
    try:
        cookie_selector = config.cookie_selector
        cookie_wait = WebDriverWait(driver, 10)
        cookie_accept = cookie_wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f"{cookie_selector}"))
        )
        cookie_accept.click()
    except:
        pass  # ! Better exception handling

    try:
        slowest_element_selector = config.slowest_element_selector
        slowest_element_wait = WebDriverWait(driver, 10)
        slowest_element_wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f"{slowest_element_selector}")
            )
        )
    except:
        pass  # ! Better exception handling

    specifications = config.specification_selector.split("¤")  # ! Better options?

    for specification in specifications:
        if specification:
            specification_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, specification))
            )
            for _ in range(3):
                try:
                    specification_element.click()
                    break
                except ElementClickInterceptedException:
                    time.sleep(1)


def get_product_from_html(
    config: Config, html: str, price_match: PriceMatch, binary_screenshot
) -> PriceMatch:
    soup = BeautifulSoup(html, "html.parser")

    for field in PriceMatch._meta.fields:
        selector_text = getattr(config, field.name + '_selector', None)

        if selector_text:
            try:
                value = ""
                if "¤" in selector_text:
                    selectors = selector_text.split("¤")
                    for selector in selectors:
                        try:
                            value += str.strip(soup.select_one(selector).text)
                        except:
                            pass
                        value += " "
                else:
                    value = str.strip(soup.select_one(selector_text).text)
                if field.name in ["shipping_price","price"]:
                    value = __extract_numbers_from_string(value)
                setattr(price_match, field.name, value)

            except AttributeError:
                setattr(price_match, field.name, None)
    price_match.product_image = binary_screenshot
    return price_match


def __get_config(url: str) -> Config:
    no_prefix = (
        url.removeprefix("http://").removeprefix("https://").removeprefix("www.")
    )
    base_url = no_prefix.split("/")[0]
    return Config.objects.get(pk=base_url)


def __extract_numbers_from_string(input_string: str) -> str:
    pattern = r"[-+]?\d{1,3}(?:,\d{3})*\.\d+|\d+"
    match = re.search(pattern, input_string)
    if match:
        return match.group().replace(',', '')
    else:
        return input_string

