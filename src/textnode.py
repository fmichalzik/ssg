from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
# Converts a TextNode to an HTMLNode, specifically a LeafNode
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")
        
# Creates Textnodes from raw markdown strings
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Initialize an empty list to store the new nodes
    nodes_list = []
    
    # Iterate over each node in the old_nodes list
    for node in old_nodes:
        # If the node's text type is not TEXT, add it to the nodes_list as is
        if node.text_type != TextType.TEXT:
            nodes_list.append(node)
            continue
        
        # Split the node's text by the delimiter
        split_list = node.text.split(delimiter)
        
        # Check if the split list has an even number of elements, which indicates a missing closing delimiter
        if len(split_list) % 2 == 0:
            raise Exception(
                "Provided delimiter is invalid Markdown syntax (missing closing delimiter)"
            )
        
        # Iterate over the split list and create new nodes
        for i in range(len(split_list)):
            if split_list[i] == "":
                continue
            if i % 2 == 1:
                # If the index is odd, create a new node with the specified text_type
                new = TextNode(split_list[i], text_type)
            else:
                # If the index is even, create a new node with the TEXT type
                new = TextNode(split_list[i], TextType.TEXT)
            # Add the new node to the nodes_list
            nodes_list.append(new)
    
    # Return the list of new nodes
    return nodes_list