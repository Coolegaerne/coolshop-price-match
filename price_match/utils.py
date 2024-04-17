import json
from price_match.models import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_website(product: Product) -> Product:
    page_source = scrape_html_from_website(product.url)
    return get_product_from_html(page_source)


def scrape_html_from_website(url: str) -> str:
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"

    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument(f"--user-agent={my_user_agent}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    wait = WebDriverWait(driver, 10)
    cookie_accept = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#coiPage-1 > div.coi-banner__page-footer > div.coi-button-group > button.coi-banner__accept")))
    cookie_accept.click()
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#site-product-price-stock-buy-container > section > div.site-product-stock-price-buy.d-flex > span > span")))

    print(driver.page_source)
    driver.quit()


def get_product_from_html(html: str) -> Product:
    pass
