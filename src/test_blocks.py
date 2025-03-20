import unittest

from blocks import markdown_to_blocks, BlockType, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph





 This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line 

- This is a list
- with items

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )
        
    def test_no_markdown_to_blocks(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [],)
        
    def test_block_eq_heading_1(self):
        block = "# This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_eq_heading_2(self):
        block = "##### This is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_not_heading_1(self):
        block = "#This is not a header so will be paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_eq_code_1(self):
        block = "```This is valid code block´```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_block_eq_code_2(self):
        block = "```            This is valid code block´```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_block_eq_code_3(self):
        block = "```" \
        "This is valid code block´" \
        "```" \
        ""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_not_code_1(self):
        block = "``This is not valid code block wo will be paragraph```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_not_code_2(self):
        block = " ```This is not valid code block wo will be paragraph```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_eq_quote(self):
        block = """>1quote
># quote
> quote
> quote
>quote"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    def test_block_not_quote(self):
        block = """>1quote
# quote
> quote
> quote
>not valid so wille be paragraph"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_eq_unordered_list(self):
        block = """- quote
- ### quote
- quote
- quote
-  valid unordered list"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_not_unordered_list(self):
        block = """- quote
- ### quote
- quote
- quote
-invalid unordered list so will be paragraph"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_eq_ordered_list(self):
        block = """1. quote
2. ### quote
3. quote
4. quote
5.  valid ordered list"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_not_ordered_list_1(self):
        block = """1. quote
2. ### quote
3. quote
4. quote
5.invalid ordered list so will be paragraph"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_not_ordered_list_2(self):
        block = """1. quote
2. ### quote
3. quote
4. quote
5 invalid ordered list so will be paragraph"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_not_ordered_list_3(self):
        block = """1. quote
2. ### quote
3. quote
4. quote
4. invalid ordered list so will be paragraph"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
if __name__ == "__main__":
    unittest.main()