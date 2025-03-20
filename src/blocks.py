from enum import Enum

# Our static site generator supports following types of markdown blocks
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

# function that takes a single block of markdown text as input
# and returns the BlockType representing the type of block it is
def block_to_block_type(block):
    # Headings start with 1-6 # characters, followed by a space

    # if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        # return BlockType.HEADING
        
    if block[:2] == "# ":
        return BlockType.HEADING
    if block[:3] == "## ":
        return BlockType.HEADING
    if block[:4] == "### ":
        return BlockType.HEADING
    if block[:5] == "#### ":
        return BlockType.HEADING
    if block[:6] == "##### ":
        return BlockType.HEADING
    if block[:7] == "###### ":
        return BlockType.HEADING
    
    # Code blocks must start with 3 backticks and end with 3 backticks
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE

    # if none of the above returns, we check for every line in a block   
    lines = block.split("\n")
    true_quote = 0
    true_unordered_list = 0
    true_ordered_list = 0
    for line in lines:
        # Every line in a quote block must start with a > character.
        if line[:1] == ">":
            true_quote += 1
        # Every line in an unordered list block must start with a - character
        if line[:2] == "- ":
            true_unordered_list += 1  
        # Every line in an ordered list block must start with a number 
        # followed by a . character and a space
        # The number must start at 1 
        if (line[:3] == f"{lines.index(line) + 1}. " 
            # and increment by 1 for each line
            and line[:1] == f"{true_ordered_list + 1}"):
            true_ordered_list += 1
    if len(lines) == true_quote:
        return BlockType.QUOTE
    if len(lines) == true_unordered_list:
        return BlockType.UNORDERED_LIST   
    if len(lines) == true_ordered_list:
        return BlockType.ORDERED_LIST
    
    # if none of the above conditions are met, the block is a normal paragraph
    return BlockType.PARAGRAPH
    

# It takes a raw Markdown string (representing a full document) as input and 
# returns a list of "block" strings.
def markdown_to_blocks(markdown) :

    # split a string into blocks based on a delimiter (\n\n is a double newline)
    blocks = markdown.split("\n\n")

    # .strip() any leading or trailing whitespace from each block
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()

    # remove any "empty" blocks due to excessive newlines.
    for block in blocks[:]:
        if not block:
            blocks.remove(block)   
    return blocks