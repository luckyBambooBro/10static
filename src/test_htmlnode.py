import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode("p")
        self.assertEqual(node.tag, "p")

    def test_values(self):
        node = HTMLNode("h1", "lorem ipsum", None, {"href": "https://google.com"})
        self.assertEqual(node.tag, "h1" )
        self.assertEqual(node.value, "lorem ipsum")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://google.com"})

    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {"href": "https://youtube.com"})
        self.assertEqual(node.props_to_html(), " href=\"https://youtube.com\"")

    def test_repr(self):
        node = HTMLNode("p", "What a strange world", None, {"class": "primary"})
        self.assertEqual(node.__repr__(), "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://google.com\">Click me!</a>")

    def test_leaf_values(self):
        node = LeafNode("h1", "lorem ipsum")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "lorem ipsum")

class TestParentNode(unittest.TestCase):
    def test_parent_values(self):
        node = ParentNode("p", [])
        self.assertEqual(node.tag, "p", [])
    
    def test_parent_to_html(self):
        child_node = LeafNode("b", "Hello, world!")
        node = ParentNode("p", [child_node], {"href": "https://google.com"})
        self.assertEqual(node.to_html(), f"<p href=\"https://google.com\"><b>Hello, world!</b></p>")

    def test_to_html_many_children(self):
        first_child = LeafNode("p", "lorem ipsum 1")
        second_child = LeafNode(None, "lorem ipsum 2")
        third_child = LeafNode("b", "lorem ipsum 3")
        parent = ParentNode("p", [
                            first_child,
                            second_child,
                            third_child
                            ])
        self.assertEqual(parent.to_html(), f"<p><p>lorem ipsum 1</p>lorem ipsum 2<b>lorem ipsum 3</b></p>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_ParentNode_repr(self):
        node = node = ParentNode("p", [], {"href": "https://google.com"})
        self.assertEqual(node.__repr__(), "ParentNode: p, children: [], {'href': 'https://google.com'}" )

if __name__ == "__main__":
    unittest.main()