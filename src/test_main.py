import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(
            extract_title("# Hello\n\nthis should not be captured"),
            "Hello"
        ) 

        self.assertEqual(
            extract_title("# Hello\nthis should be captured"),
            "Hello\nthis should be captured"
        ) 

        self.assertEqual(
            extract_title("some text prior # Hello\nthis should be captured"),
            "Hello\nthis should be captured"
        ) 