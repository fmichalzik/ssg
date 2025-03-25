import unittest

from markdown_to_html import markdown_to_html_node

class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading(self):
        heading = """
# This is **bolded** paragraph
text in a p
tag here

## This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(heading)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is <b>bolded</b> paragraph text in a p tag here</h1><h2>This is another paragraph with <i>italic</i> text and <code>code</code> here</h2></div>",
        )
        
    def test_heading(self):
        heading = """
# This is **bolded** paragraph
text in a p
tag here

## This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(heading)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is <b>bolded</b> paragraph text in a p tag here</h1><h2>This is another paragraph with <i>italic</i> text and <code>code</code> here</h2></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_codeblock2(self):
        md = "```This is short code block```"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is short code block</code></pre></div>",
        )
    
    def test_quoteblock(self):
        md = """
>"I am in fact a Hobbit in all but size."
>
>-- J.R.R. Tolkien
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>"I am in fact a Hobbit in all but size."  -- J.R.R. Tolkien</blockquote></div>'
        )

    def test_unordered_list(self):
        md = """
- "I am in fact a **Hobbit** in all but size."
- Test
- J.R.R. _Tolkien_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>"I am in fact a <b>Hobbit</b> in all but size."</li><li>Test</li><li>J.R.R. <i>Tolkien</i></li></ul></div>'
        )
    
    def test_ordered_list(self):
        md = """
1. "I am in fact a **Hobbit** in all but size."
2. This is text with a link [to boot dev](https://www.boot.dev)
3. J.R.R. _Tolkien_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ol><li>"I am in fact a <b>Hobbit</b> in all but size."</li><li>This is text with a link <a href="https://www.boot.dev">to boot dev</a></li><li>J.R.R. <i>Tolkien</i></li></ol></div>'
        )

if __name__ == "__main__":
    unittest.main()