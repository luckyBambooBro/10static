import unittest
from inline_markdown import (
    split_nodes_delimiter, 
    split_nodes_img, 
    split_nodes_link, 
    extract_markdown_links, 
    extract_markdown_images
)

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

class test_Extract_img_and_link_regexes(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(text, [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])

    def test_extract_markdown_links(self):
        text = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(text, [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')])
    
    def test_split_link_nodes(self):
        nodes = [TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT),
    TextNode("This is text with a `code block` word", TextType.TEXT),
    TextNode("and this is some bold text", TextType.BOLD)
]
        self.assertEqual(split_nodes_link(nodes), [
            TextNode("This is text with a link ", TextType.TEXT), 
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
            TextNode(" and ", TextType.TEXT), 
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("and this is some bold text", TextType.BOLD)
        ])

    def test_split_image_nodes(self):
        nodes = [TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    ),
    TextNode("and here's some italicised text", TextType.ITALIC)
]
        self.assertEqual(split_nodes_img(nodes), [
            TextNode("This is text with an ", TextType.TEXT), 
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode("and here's some italicised text", TextType.ITALIC)])