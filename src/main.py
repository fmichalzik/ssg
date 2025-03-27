
from utils import get_filepaths_from_source, delete_all_in_target, copy_files_to_target
from pagegenerator import generate_page

def main():

    source_path = "static"
    target_path = "public"
 
    file_paths = get_filepaths_from_source(source_path)
    delete_all_in_target(target_path)
    copy_files_to_target(file_paths, target_path)

    md_path = "content/index.md"
    template_path = "template.html"
    dest_path = "public/"
    generate_page(md_path, template_path, dest_path)

main()