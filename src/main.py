from textnode import TextNode, TextType
import os
import shutil

def main():

    source_path = "static"
    target_path = "public"



    def delete_all_in_target(target_path):
        # if the folder exists - delete all the content
        if os.path.exists(f"{target_path}"):
            shutil.rmtree(f"{target_path}")
            print("Delete Target: Target folder deleted.")
        else:
            print(f"Delete Target: Folder {target_path} does not exist")

    def get_filepaths_from_source(source_path):
        # list all entries detected @ path
        # these can be files and folders
        entries = os.listdir(source_path)

        # if no entries detected - return
        if not entries:
            print(f"No entries detected at path {source_path}")
            return 
        
        print(f"Following entries detected: {entries}")
        # create a new new list to store final file paths
        file_paths = []

        # iterate over entries to check wether it is a file or a folder, otherwise raise Exception
        for entrie in entries:
            # create path to entrie
            entrie_path = os.path.join(source_path, entrie)
            # if entrie is a file, store file path in file_paths list
            if os.path.isfile(entrie_path):
                print(f"entrie at path {entrie_path} detected as a file and added to file_path list")
                file_paths.append(entrie_path)
            # if entrie is a folder, recursive call and extend returned file_paths list of recursion to file_paths list 
            elif os.path.isdir(entrie_path):
                print(f"entrie at path {entrie_path} detected as a folder and so recursive call on that")
                file_paths.extend(get_filepaths_from_source(entrie_path))
            else:
                raise Exception(f"No file or folder detected at path {entrie_path}")
        
        # Returns a list with filepaths the entries @ path
        print(f"final file_paths list: {file_paths}")
        return file_paths

    def copy_files_to_target(file_paths, target_path):
        if not os.path.exists(target_path):
            print(f"Create target folder {target_path}")
            os.mkdir(target_path)
        if not file_paths:
            print(f"No files")
            return
        # Iterate over files in file_paths 
        for file_path in file_paths:
            # we need a split path in order to work with subdirectories
            split_path = file_path.split("/")
            # if split_path > 2 there are subdirectories (1 beeing the source folder and 2 the file itself)
            if len(split_path) > 2:
                for i in range(1, len(split_path) - 1):
                    target_path = os.path.join(target_path, split_path[i])
                    os.mkdir(target_path)
            new_file = shutil.copy(file_path, target_path)
            print(f"Created new file at filepath {new_file}")   
    
    file_paths = get_filepaths_from_source(source_path)
    delete_all_in_target(target_path)
    copy_files_to_target(file_paths, target_path)
        

main()