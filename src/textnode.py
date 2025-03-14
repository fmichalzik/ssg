from enum import Enum
from htmlnode import LeafNode
from utils import extract_markdown_links, extract_markdown_images

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

# The following functions are neede to split raw markdown text into TextNodes based on images and links
def split_nodes_image(old_nodes):
    # Initialize an empty list to store the new nodes
    nodes_list = []
    
    # Iterate over each node in the old_nodes list
    for node in old_nodes:
        # If the node's text type is not TEXT, add it to the nodes_list as is
        if node.text_type != TextType.TEXT:
            nodes_list.append(node)
            continue
        # Don't append any TextNodes that have empty text to the final list
        if not node.text:
            continue

        # So we save the node text in a 'sections' variable to work on 
        # later sections will be a split list of the text
        sections = node.text

        # Then we extract alt/image to use them as delimite to split sections
        images = extract_markdown_images(node.text)

        # We itarte for the amount of extracted links
        for i in range(0, len(images)):
            # Save the link(tuple) values 
            alt = images[i][0]
            image = images[i][1]
            # Split sections at the point of the link values 
            # in the first i, this will split the node.text
            sections = sections.split(f"![{alt}]({image})", 1)

            # if there is text "befor" the split, add it as TextType to the nodes_list 
            if sections[0]:
                nodes_list.append(TextNode(sections[0], TextType.TEXT))
            
            # add the first iteration of link values as TextType to the nodes_list
            nodes_list.append(TextNode(alt, TextType.IMAGE, image))

            # Set sections to text "after" the split for the next iteration
            sections = sections[1]

        # if there is a text after the last link, add it as TextType to the nodes_list   
        if sections:
            nodes_list.append(TextNode(sections, TextType.TEXT))

    return nodes_list

def split_nodes_link(old_nodes):
    # Initialize an empty list to store the new nodes
    nodes_list = []
    
    # Iterate over each node in the old_nodes list
    for node in old_nodes:
        # If the node's text type is not TEXT, add it to the nodes_list as is
        if node.text_type != TextType.TEXT:
            nodes_list.append(node)
            continue
        # Don't append any TextNodes that have empty text to the final list
        if not node.text:
            continue

        # So we save the node text in a 'sections' variable to work on 
        # later sections will be a split list of the text
        sections = node.text

        # Then we extract link/linktext to use them as delimite to split sections
        links = extract_markdown_links(node.text)

        # We itarte for the amount of extracted links
        for i in range(0, len(links)):
            # Save the link(tuple) values 
            link_text = links[i][0]
            link = links[i][1]
            # Split sections at the point of the link values 
            # in the first i, this will split the node.text
            sections = sections.split(f"[{link_text}]({link})", 1)

            # if there is text "befor" the split, add it as TextType to the nodes_list 
            if sections[0]:
                nodes_list.append(TextNode(sections[0], TextType.TEXT))
            
            # add the first iteration of link values as TextType to the nodes_list
            nodes_list.append(TextNode(link_text, TextType.LINK, link))

            # Set sections to text "after" the split for the next iteration
            sections = sections[1]

        # if there is a text after the last link, add it as TextType to the nodes_list   
        if sections:
            nodes_list.append(TextNode(sections, TextType.TEXT))

    return nodes_list