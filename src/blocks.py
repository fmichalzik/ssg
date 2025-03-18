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
            function
    return blocks