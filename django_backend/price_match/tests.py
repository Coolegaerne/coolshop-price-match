from django.test import TestCase
from .utils import find_ean_in_string, extract_numbers_from_string, get_product_from_html
from parameterized import parameterized
from unittest.mock import MagicMock


class EANTestCases(TestCase):
    #Arrange
    @parameterized.expand([
        ("This input string contains a valid EAN: 5594962001960.", "5594962001960"),
        ("This string does not contain a valid EAN.", None),
        ("Test text 5594962001960 and some text", "5594962001960"),
        ("find First EAN 5323296204450 and second EAN 9876543210987.","5323296204450"),
        ("Invalid EAN: 12345abcde678 fafsfasf.", None)
    ]) 

    def test_find_ean_in_string(self, input_string, expected_output):
        #Act
        result = find_ean_in_string(input_string)
        #Assert
        self.assertEqual(result, expected_output)


class ExtractPriceFromStringTestCases(TestCase):
    #Arrange
    @parameterized.expand([
        ("The price is 2,234.56 kr.", "2234.56"),
        ("No numbers here", "No numbers here")
    ])

    def test_numbers_extracted(self, input_string, expected_output):
        #Act
        result = extract_numbers_from_string(input_string)
        #Assert
        self.assertEqual(result, expected_output)


class MockConfig:
    base_url = "proshop.dk"
    slowest_element_selector = ".site-currency-attention"
    cookie_selector = "#coiPage-1 > div.coi-banner__page-footer > div.coi-button-group > button.coi-banner__accept"
    specification_selector = ""
    price_selector = ".site-currency-attention"
    name_selector = "#site-product-price-stock-buy-container > h1"
    stock_status_selector = ".site-stock > .status"
    shipping_price_selector = ".site-stock > .shipping"
    currency = "dkk"


class TestGetProductFromHTML(TestCase):
    def test_get_product_from_html(self):
        
        #Arrange
        mock_config = MockConfig()
        #Simulate an HTML page
        mock_html = """ 
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Proshop Product</title>
            </head>
            <body>
                <div id="site-product-price-stock-buy-container">
                    <h1>Product Title</h1>
                    <div class="site-stock">
                        <div class="shipping">Shipping: 20 DKK</div>
                        <div class="status">In Stock</div>
                        <div>Other Info</div>
                    </div>
                </div>
                <div class="site-currency-attention">Product Price: 500 DKK</div>
                <div class="coi-banner__page-footer">
                    <div class="coi-button-group">
                        <button class="coi-banner__accept">Accept Cookies</button>
                    </div>
                </div>
            </body>
            </html>
            """
        mock_price_match = MagicMock()
        mock_binary_screenshot = b'mocked_screenshot'

        #Act
        result = get_product_from_html(mock_config, mock_html, mock_price_match, mock_binary_screenshot)

        #Assert
        self.assertEqual(result, mock_price_match) 
        self.assertEqual(mock_price_match.price, "500")  
        self.assertEqual(mock_price_match.shipping_price, "20")
        self.assertEqual(mock_price_match.name, "Product Title")
        self.assertEqual(mock_price_match.stock_status, "In Stock")
