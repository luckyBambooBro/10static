import unittest
from textnode import TextNode, TextType
from extract_MD_img_and_link import extract_markdown_images, extract_markdown_links, split_nodes_link

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