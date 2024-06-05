from django.test import TestCase
from .utils import find_ean_in_string, extract_numbers_from_string, get_product_from_html
from .models import Config, PriceMatch


class PriceMatchTestCases(TestCase):
    def test_ean_found(self):
        #Arrange 
        input_string = "This input string contains a valid EAN: 5594962001960."
        expected_output = "5594962001960"

        #Act
        result = find_ean_in_string(input_string)

        #Assert
        self.assertEqual(result, expected_output)


    def test_ean_notfound(self):
        #Arrange
        input_string = "This string does not contain a valid EAN."
        expected_output = None

        #Act
        result = find_ean_in_string(input_string)

        #Assert 
        self.assertEqual(result, expected_output)


    def test_ean_in_middel_of_string(self):
        #Arrange
        input_string = "Test text 5594962001960 and some text"
        expected_output = "5594962001960"

        #Act
        result = find_ean_in_string(input_string)

        #Assert
        self.assertEqual(result, expected_output)


    def test_multiple_eans_in_string(self):
        #Arrange
        input_string = "find First EAN 5323296204450 and second EAN 9876543210987."
        expected_output = "5323296204450"

        #Act 
        result = find_ean_in_string(input_string)

        #Assert
        self.assertEqual(result, expected_output)

    def test_ean_with_non_digits(self):
        #Arrange
        input_string = "Invalid EAN: 12345abcde678 fafsfasf."
        expected_output = None

        #Act
        result = find_ean_in_string(input_string)

        #Assert
        self.assertEqual(result, expected_output)


    #Tests for method "extract_numbers_from_string"
    def test_numbers_extracted(self):
        #Arrange
        input_string = "The price is $1,234.56"
        expected_output = "1234.56"

        #Act
        result = extract_numbers_from_string(input_string)

        #Assert
        self.assertEqual(result, expected_output)


    def test_no_numbers(self):
        #Arrange
        input_string = "No numbers here"
        expected_output = "No numbers here"

        #Act
        result = extract_numbers_from_string(input_string)

        #Assert
        self.assertEqual(result, expected_output)