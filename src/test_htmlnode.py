import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()