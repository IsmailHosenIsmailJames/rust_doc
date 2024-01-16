import os
import json

def create_folder_file_map(folder_path):
    """
    Creates a nested map representing the folder structure and files, where:
    - Keys are folder names.
    - Values are either nested maps (for subfolders) or lists of file names.
    """

    folder_map = {}
    for root, directories, files in os.walk(folder_path):
        relative_path = root.replace(folder_path, '').strip(os.sep)  # Get relative path
        current_map = folder_map
        for directory in relative_path.split(os.sep):
            current_map = current_map.setdefault(directory, {})  # Create nested maps for subfolders
        cpFiles = files[::]
        for i in range(len(cpFiles)):
            currentFileSplited = f"{cpFiles[i]}".split(".")
            currentFileExtension = currentFileSplited[len(currentFileSplited)-1]
            if(currentFileExtension != "html"):
                files.remove(cpFiles[i])
        for i in (range(len(files))):
            files[i] = files[i].replace("assets/", "")

        if(len(files) > 0):
            current_map['files'] = files  # Add files to the leaf node

    return folder_map

def save_map_as_json(folder_map, output_file):
    """
    Saves a nested map to a JSON file.
    """

    with open(output_file, 'w') as f:
        json.dump(folder_map, f, indent=4)  # Indent for readability

# Example usage:
folder_path = 'assets'
output_file = 'onlyHTMLFilesMap.json'

folder_map = create_folder_file_map(folder_path)
save_map_as_json(folder_map, output_file)

print("Folder and file map saved to:", output_file)
