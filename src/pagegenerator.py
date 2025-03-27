from utils import read_from_file, write_to_file
from markdown_to_html import markdown_to_html_node, extract_title

# will generate a webpage using a html template and a md file
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file / template and store it
    md = read_from_file(from_path)
    template = read_from_file(template_path)

    # Use your markdown_to_html_node function and .to_html() method 
    # to convert the markdown file to an HTML string
    html_string = markdown_to_html_node(md).to_html()
    html_title = extract_title(md)

    # replaces {{ Title }} and {{ Content }} placeholders in the template with the HTML and title
    template = template.replace("{{ Title }}", html_title).replace("{{ Content }}", html_string)

    # Writes the new full HTML page to a file at dest_path
    write_to_file(dest_path, template)

    print(f"Page generated")
    
    
