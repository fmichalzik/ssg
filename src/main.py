
import sys
from utils import get_filepaths_from_source, delete_all_in_target, copy_files_to_target
from pagegenerator import generate_pages_recursive

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'

    source_path = "./static"
    target_path = "./docs"

 
    file_paths = get_filepaths_from_source(source_path)
    delete_all_in_target(target_path)
    copy_files_to_target(file_paths, target_path)

    md_path = "./content"
    template_path = "./template.html"
    dest_path = "./docs"
    generate_pages_recursive(md_path, template_path, dest_path, basepath)

main()