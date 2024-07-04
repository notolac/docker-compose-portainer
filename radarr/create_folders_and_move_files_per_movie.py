import os
import shutil


def organize_files(source_folder):
    # Verify that the source folder exists
    if not os.path.isdir(source_folder):
        print(f"The folder {source_folder} does not exist.")
        return

    # Iterate over all files in the source folder
    for name in os.listdir(source_folder):
        full_path = os.path.join(source_folder, name)

        # Verify that it is a file (not a folder)
        if os.path.isfile(full_path):
            # Get the file name without the extension
            name_without_extension = os.path.splitext(name)[0]

            # Create a new folder with the file name without the extension
            new_folder = os.path.join(source_folder, name_without_extension)
            os.makedirs(new_folder, exist_ok=True)

            # Move the file to the new folder
            new_file_path = os.path.join(new_folder, name)
            shutil.move(full_path, new_file_path)

            print(f"File {name} moved to {new_folder}")


# Specify the path of the source folder
source_folder = 'path/to/your/source/folder'
organize_files(source_folder)
