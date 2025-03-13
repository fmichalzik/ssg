# In utils will be special functions to help us with processing data, 
# eg function extract the links and images from our Markdown using regex

import re

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" ,text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" ,text)
    return matches