import unittest
from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType

class testSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        new_nodes = split_nodes_delimiter([TextNode("This is text with a `code block` word", TextType.TEXT)], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode('code block', TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_split_nodes_delimiter_start_word(self):
        new_nodes = split_nodes_delimiter([TextNode("`This` is text with a code block word", TextType.TEXT)], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This", TextType.CODE), TextNode(' is text with a code block word', TextType.TEXT)])

    def test_split_nodes_delimiter_end_word(self):
        new_nodes = split_nodes_delimiter([TextNode("This is text with a code block `word`", TextType.TEXT)], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a code block ", TextType.TEXT), TextNode('word', TextType.CODE)])

    def test_split_nodes_delimiter_2_delimiter_sets(self):
        new_nodes = split_nodes_delimiter([TextNode("This is text with a `code block` word ... and `another code block`", TextType.TEXT)], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode('code block', TextType.CODE), TextNode(" word ... and ", TextType.TEXT), TextNode("another code block", TextType.CODE)])