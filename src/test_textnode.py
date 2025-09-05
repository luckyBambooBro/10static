import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_different_url(self):
        node = TextNode("This is a text node", TextType.TEXT, url="google.com")
        node2 = TextNode("This is a text node", TextType.TEXT, url="youtube.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_image(self):
        node = TextNode("lorem ipsum image", TextType.IMAGE, "https://images.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")    
        self.assertEqual(html_node.props, {"src": "https://images.google.com", "alt": "lorem ipsum image"})
        self.assertEqual(html_node.props_to_html(), f" src=\"https://images.google.com\" alt=\"lorem ipsum image\"")
        
if __name__ == "__main__":
    unittest.main()
