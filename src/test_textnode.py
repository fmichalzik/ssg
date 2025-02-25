import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a different text", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.CODE)
        node5 = TextNode("This is a text node", TextType.CODE, None)
        node6 = TextNode("This is a text node", TextType.CODE, "https://www.boot.dev")
        self.assertEqual(node, node2)
        self.assertEqual(node4, node5)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node2, node4)
        self.assertNotEqual(node5, node6)


if __name__ == "__main__":
    unittest.main()
