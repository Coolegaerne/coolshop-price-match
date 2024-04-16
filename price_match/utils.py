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
    chrome_options.headless = False
    chrome_options.add_argument(f"--user-agent={my_user_agent}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    with open("C:/Users/olive/OneDrive/Dokumenter/dev/coolshop-price-match/price_match/cookies/proshop_cookies.json", 'r') as file:
        cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

    wait = WebDriverWait(driver, 10)

    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#site-product-price-stock-buy-container > section > div.site-product-stock-price-buy.d-flex > span > span")))
    name = driver.find_element(By.CSS_SELECTOR, "#site-product-price-stock-buy-container > h1")

    print(element.text)
    print(name.text)

    driver.quit()


def get_product_from_html(html: str) -> Product:
    pass

def extract_cookies_from_website(url: str) -> None:
    my_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"

    chrome_options = Options()
    chrome_options.headless = False
    chrome_options.add_argument(f"--user-agent={my_user_agent}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(EC.title_contains("1983629247h"))
    except:
        pass

    all_cookies = driver.get_cookies()
    print(all_cookies)