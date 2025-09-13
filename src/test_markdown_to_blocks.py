import unittest
from markdown_to_blocks import markdown_to_blocks, Blocktype, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlock(unittest.TestCase):
    def test_block_to_block(self):
        self.assertEqual(block_to_block_type("# My Favourite Books"), Blocktype.HEADING)
        self.assertEqual(block_to_block_type("``` print(\"hello world\")\n```"), Blocktype.CODE)
        self.assertEqual(block_to_block_type("> luck is when preparation meets opportunity"), Blocktype.QUOTE)
        self.assertEqual(block_to_block_type("- bread\n- tomatoes\n- cucumber"), Blocktype.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. bread\n2. tomatoes\n3. cucumber"), Blocktype.ORDERED_LIST)
        self.assertEqual(block_to_block_type("lorem ipsum"), Blocktype.PARAGRAPH)