from blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode
from textnode import text_to_textnodes, text_node_to_html_node, TextNode, TextType

# converts a full markdown document into a single parent HTMLNode. 
# That one parent HTMLNode should (obviously) contain many child HTMLNode objects representing the nested elements.

def markdown_to_html_node(markdown):
    def get_nodes(markdown):
        nodes = []
        # Split the markdown into blocks
        markdown_blocks = markdown_to_blocks(markdown)
        # Loop over each block
        for block in markdown_blocks:

            # Determine the type of block
            block_type = block_to_block_type(block)
            # Based on the type of block, create a new HTMLNode with the proper data
            match block_type:

                case BlockType.PARAGRAPH:
                    # newlines within a paragraph block are typically converted to spaces in the final HTML
                    block = block.replace("\n", " ")
                    # Paragraphs should be surrounded by a <p> tag
                    child_nodes = text_to_children(block)
                    parent_node = ParentNode("p", child_nodes)
                    nodes.append(parent_node)
                
                case BlockType.HEADING:
                    # newlines within a header should be converted to space
                    block = block.replace("\n", " ")
                    # Headings should be surrounded by a <h1> to <h6> tag
                    # depending on the number of # characters
                    num_of_hashtags = 0
                    for i in range(0, 6):
                        if block[i] == '#':
                            num_of_hashtags += 1
                    block = block[num_of_hashtags:]
                    # removes the space after header hashtags
                    if block[0] == " ":
                        block = block[1:]
                    child_nodes = text_to_children(block)
                    parent_node = ParentNode(f"h{num_of_hashtags}", child_nodes)
                    nodes.append(parent_node)
                
                case BlockType.CODE:
                    # Remove the triple backticks
                    # Extract just the content between them
                    block = block[3:-3:]
                    # If there's a newline at the beginning of that content we trim it
                    block = block.lstrip("\n")
                    # remove leading whitespaces
                    if block[0] == " ":
                        block = block[1:]
                    code_node = TextNode(block, TextType.CODE)
                    parent_node = ParentNode("pre", [text_node_to_html_node(code_node)])
                    nodes.append(parent_node)

                case BlockType.QUOTE:
                    # newlines within a quote block are typically converted to spaces in the final HTML
                    child_nodes = block.split("\n")
                    for i in range(len(child_nodes)):
                        if child_nodes[i].startswith(">"):
                            child_nodes[i] = child_nodes[i][1:]

                    block = " ".join(child_nodes)


                    #block = block.replace("\n", " ")
                    #block = block.lstrip(">")
                    #block = block.replace(">")
                    # Paragraphs should be surrounded by a <blockquote> tag
                    child_nodes = text_to_children(block)
                    parent_node = ParentNode("blockquote", child_nodes)
                    nodes.append(parent_node)

                case BlockType.UNORDERED_LIST:
                    #  each list item should be surrounded by a <li> tag.
                    child_nodes = block.split("\n")
                    for i in range(len(child_nodes)):
                        child_nodes[i] = child_nodes[i][2:] # trims the "- " at the beginning of each
                        child_nodes[i] = text_to_children(child_nodes[i])
                        child_nodes[i] = ParentNode("li", child_nodes[i])
                    # Unordered list blocks should be surrounded by a <ul> tag
                    parent_node = ParentNode("ul", child_nodes)
                    nodes.append(parent_node)

                case BlockType.ORDERED_LIST:
                    #  each list item should be surrounded by a <li> tag.
                    child_nodes = block.split("\n")
                    for i in range(len(child_nodes)):
                        child_nodes[i] = child_nodes[i][3:] # trims the "x. " at the beginning of each
                        child_nodes[i] = text_to_children(child_nodes[i])
                        child_nodes[i] = ParentNode("li", child_nodes[i])
                    # Unordered list blocks should be surrounded by a <ol> tag
                    parent_node = ParentNode("ol", child_nodes)
                    nodes.append(parent_node)

        return nodes
                
    
    def wrap_nodes_in_div(nodes):
        return ParentNode("div", nodes)
    
    # test = wrap_nodes_in_div(get_nodes(markdown))
    # print(test.to_html())
    return wrap_nodes_in_div(get_nodes(markdown))

def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes