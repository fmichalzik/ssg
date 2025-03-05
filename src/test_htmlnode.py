import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_child_and_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        another_child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node, another_child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><span>child</span></div>",
        )

    def test_to_html_with_xchild_and_xgrandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        another_grandchild_node = LeafNode("p", "another grandchild")
        another_child_node = ParentNode("span", [another_grandchild_node])
        parent_node = ParentNode("div", [child_node, another_child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><span><p>another grandchild</p></span></div>",
        )

    def test_to_html_with_children_and_props(self):
        child_node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><a href="https://www.google.com">Hello, world!</a></div>')

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_children(self):
        parent = ParentNode("div", [
            ParentNode("section", [
                ParentNode("article", [
                    LeafNode("p", "Text")
                ])
            ])
        ])
        self.assertEqual(
            parent.to_html(),
            "<div><section><article><p>Text</p></article></section></div>"
        )


if __name__ == "__main__":
    unittest.main()