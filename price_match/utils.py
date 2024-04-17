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
    
    config_file = __get_config_file(url)

    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument(f"--user-agent={my_user_agent}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    cookie_selector = config_file.get("cookie_selector")
    wait = WebDriverWait(driver, 10)
    cookie_accept = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"{cookie_selector}")))
    cookie_accept.click()
    
    price_selector = config_file.get("price_selector")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"{price_selector}")))

    page_source = driver.page_source
    driver.quit()
    return page_source


def get_product_from_html(html: str) -> Product:
    pass


def __get_config_file(url: str) -> dict:
    base_url = url.split("/")[2].removeprefix("www.")
    file_path = f"price_match/website_configs/{base_url}.json"
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Config file for {base_url} not found.")
        return None