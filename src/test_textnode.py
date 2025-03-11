import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.CODE)
        node5 = TextNode("This is a text node", TextType.CODE, None)
        self.assertEqual(node, node2)
        self.assertEqual(node4, node5)

    def test_eq_false(self):
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a different text", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.CODE)
        node5 = TextNode("This is a text node", TextType.CODE, None)
        node6 = TextNode("This is a text node", TextType.CODE, "https://www.boot.dev")
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node2, node4)
        self.assertNotEqual(node5, node6)

    def test_eq_url(self):
        node6 = TextNode("This is a text node", TextType.CODE, "https://www.boot.dev")
        node7 = TextNode("This is a text node", TextType.CODE, "https://www.boot.dev")
        self.assertEqual(node6, node7)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, normal, https://www.boot.dev)", repr(node)
        )
    
class TestTextNodeToHTMLNode(unittest.TestCase):   
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")    
    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")  
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "image.url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.url", "alt": "alt text"})

class TestSplitDelimiter(unittest.TestCase):
    def test_no_split(self):
        node = TextNode("This is a text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.TEXT)
        self.assertEqual(new_nodes, [node])
        
    def test_code_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),   
        ])

    def test_bold_split(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),   
        ])

    def test_delimiters_at_end(self):
        node = TextNode("This is text with last word _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with last word ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),  
        ])

    def test_missing_closing_delimiter(self):
        node = TextNode("This text is **missing* an end delimiter", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            str(context.exception), 
            "Provided delimiter is invalid Markdown syntax (missing closing delimiter)"
        )

    def test_multiple_code_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node1 = TextNode("This is another text with a `code block` and another `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node1], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is another text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and another ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ])

    def test_empty_content(self):
        node = TextNode("This is text with no _ _ italic word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with no ", TextType.TEXT),
            TextNode(" ", TextType.ITALIC),
            TextNode(" italic word", TextType.TEXT),
        ])

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()
