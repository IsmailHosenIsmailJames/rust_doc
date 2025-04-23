import os
import json

def find_indexed_folders(current_dir):
    """
    Recursively scans a directory and its subdirectories.
    Builds a nested map of folders that contain an 'index.html' file,
    or contain subfolders that eventually lead to an 'index.html'.

    Args:
        current_dir (str): The absolute path of the directory to scan.

    Returns:
        dict: A nested dictionary representing the folder structure.
              Keys are folder names. Values are dictionaries containing:
              - 'parent' (str): Absolute path of the parent directory.
              - 'index_path' (str, optional): Absolute path to index.html if present.
              - 'children' (dict): Nested map of qualifying subfolders.
              Returns an empty dict if no qualifying folders are found within.
    """
    children_map = {}
    # Check if the current path is a valid directory
    if not os.path.isdir(current_dir):
        # This case should ideally not be hit if called correctly initially,
        # but good for safety during recursion on potentially broken symlinks etc.
        return children_map

    try:
        # List items (files and folders) in the current directory
        items = os.listdir(current_dir)
    except OSError as e:
        # Handle potential permission errors
        print(f"Warning: Could not access '{current_dir}'. Skipping. Error: {e}")
        return children_map # Return empty map for this branch

    for item in items:
        # Construct the full path for the item
        item_path = os.path.join(current_dir, item)

        # Process only if the item is a directory
        if os.path.isdir(item_path):
            sub_dir_name = item # The name of the subfolder
            index_file_path = os.path.join(item_path, 'index.html')
            # Check specifically if 'index.html' exists AND is a file
            has_index = os.path.isfile(index_file_path)

            # --- Recursive Call ---
            # Find qualifying folders *within* this subdirectory first
            nested_children = find_indexed_folders(item_path)
            # ----------------------

            # --- Decision Logic ---
            # Include this folder in the map IF:
            # 1. It directly contains 'index.html'
            # OR
            # 2. It has children (or grandchildren, etc.) that qualified
            if has_index or nested_children:
                folder_data = {
                    # Store the absolute path of the immediate parent directory
                    'parent': current_dir,
                    # Store the map of qualifying children found by the recursive call
                    'children': nested_children
                }
                # Add the index.html path only if it actually exists in *this* folder
                if has_index:
                    folder_data['index_path'] = index_file_path

                # Add this folder's data to the map of its parent
                children_map[sub_dir_name] = folder_data
            # --- End Decision ---

    # Return the map of qualifying children found in 'current_dir'
    return children_map

# --- Main Execution ---
if __name__ == "__main__":
    root_folder_name = 'assets/html'  # The starting folder name
    output_json_file = 'folder_map.json'

    # Get the absolute path to the root folder for consistency
    start_path = os.path.abspath(root_folder_name)

    # Check if the root folder exists
    if not os.path.isdir(start_path):
        print(f"Error: Root folder '{start_path}' not found.")
        exit(1) # Exit with an error code

    print(f"Scanning folder: '{start_path}'...")

    final_map = {} # This will hold the final complete map

    # --- Handle the Root Folder Separately ---
    # The recursive function processes *children* of the given dir.
    # We need to check the root folder itself too.
    root_index_path = os.path.join(start_path, 'index.html')
    root_has_index = os.path.isfile(root_index_path)

    # Call the recursive function to process the children of the root
    root_children = find_indexed_folders(start_path)

    # Decide if the root folder itself should be included in the final map
    if root_has_index or root_children:
        # Create the data structure for the root folder
        root_data = {
            # The parent of the root folder
            'parent': os.path.dirname(start_path),
            'children': root_children
        }
        if root_has_index:
            root_data['index_path'] = root_index_path

        # The final map's top-level key will be the root folder's name
        final_map[root_folder_name] = root_data
    # --- End Root Handling ---

    # Save the resulting map to a JSON file
    try:
        with open(output_json_file, 'w', encoding='utf-8') as f:
            # Use indent for pretty printing, ensure_ascii=False for non-latin chars
            json.dump(final_map, f, indent=4, ensure_ascii=False)
        print(f"Successfully created folder map in '{output_json_file}'")
    except IOError as e:
        print(f"Error writing JSON file '{output_json_file}': {e}")
        exit(1)
    except TypeError as e:
        # This might happen if non-serializable data somehow gets into the map
        print(f"Error serializing data to JSON: {e}")
        exit(1)