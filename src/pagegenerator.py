from utils import read_from_file, write_to_file
from markdown_to_html import markdown_to_html_node, extract_title
import os, pathlib

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

def generate_pages_recursive(from_path, template_path, dest_path):
    print(f"Generating pages recursivly ...")

    # generates list with filepaths in directory
    files = os.listdir(from_path)

    # crawls every entry in directory to check wether it es a .md file or another directory
    for file in files:
        current_filepath = os.path.join(from_path, file)
        target_filepath = os.path.join(dest_path, file)
        print(current_filepath)
        # check if it is a .md file
        if os.path.isfile(current_filepath) and pathlib.Path(file).suffix == ".md":
            # if it is .md file generate page in dest_path using template
            generate_page(current_filepath, template_path, dest_path)

        # check if it is another directory
        elif os.path.isdir(current_filepath):
            # if it is another directory, recursion crawl in nested directory
            generate_pages_recursive(current_filepath, template_path, target_filepath)

        # if its none if the above, continue
        else:
            continue