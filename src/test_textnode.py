import unittest

from textnode import TextNode, TextType


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
        node = TextNode("This is a text node", TextType.NORMAL, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, normal, https://www.boot.dev)", repr(node)
        )

if __name__ == "__main__":
    unittest.main()
