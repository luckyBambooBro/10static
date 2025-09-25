import unittest
from generate_page import extract_title

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

        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(actual, "title")

        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")


    def test_none(self):
        try:
            extract_title(
                """
no title
"""
            )
            self.fail("Should have raised an exception")
        except Exception as e:
            pass