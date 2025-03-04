import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        child_node = [HTMLNode("p", "This is a child node")]
        props = {"href": "https://www.google.com"}
        node = HTMLNode("h1", "This is a html node", child_node, props)
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "This is a html node")
        self.assertEqual(node.children, child_node)
        self.assertEqual(node.props, props)

    def test_repr(self):
        node = HTMLNode("p", "This is a html node")
        self.assertEqual( 
            "HTMLNode(p, This is a html node, None, None)", repr(node)
        )

    def test_props_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode("p", "This is a html node", None, props)
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )

    def test_leaf_values(self):
        leaf_node = LeafNode("p", "This is a leaf node", {"href": "https://www.google.com"})
        self.assertEqual(leaf_node.tag, "p")
        self.assertEqual(leaf_node.value, "This is a leaf node")
        self.assertEqual(leaf_node.props, {"href": "https://www.google.com"})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Hello, world!</a>'
            )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_repr(self):
        node = LeafNode("p", "This is a leaf node")
        self.assertEqual( 
            "LeafNode(p, This is a leaf node, None)", repr(node)
        )

if __name__ == "__main__":
    unittest.main()