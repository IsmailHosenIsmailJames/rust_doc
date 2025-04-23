import os
import json # For pretty-printing the output

def find_folders_with_index(root_dir):
    """
    Recursively scans a directory structure starting from root_dir.
    Creates a list of dictionaries for folders containing an 'index.html' file.

    Args:
        root_dir (str): The path to the starting folder (e.g., 'html').

    Returns:
        list: A list of dictionaries. Each dictionary represents a folder
              containing 'index.html' and includes:
              - 'folder_name': The name of the folder.
              - 'parent_folder_path': The absolute path of the parent directory.
              - 'folder_full_path': The absolute path of the folder itself.
              - 'index_html_path': The absolute path to the 'index.html' file.
              Returns an empty list if the root directory doesn't exist or
              no matching folders are found. Returns None if root_dir is not a directory.
    """
    # Check if the provided root directory exists and is actually a directory
    if not os.path.isdir(root_dir):
        print(f"Error: Root directory '{root_dir}' not found or is not a directory.")
        return None # Indicate an issue

    folders_with_index = []
    abs_root_dir = os.path.abspath(root_dir) # Get absolute path for consistency

    # os.walk iterates through the directory tree
    # dirpath: current directory path
    # dirnames: list of subdirectories in dirpath
    # filenames: list of files in dirpath
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        # Check if 'index.html' exists in the list of files for the current directory
        if 'index.html' in filenames:
            abs_dirpath = os.path.abspath(dirpath)
            folder_name = os.path.basename(abs_dirpath)

            # Get the parent directory path
            parent_path = os.path.dirname(abs_dirpath)

            # Construct the full path to the index.html file
            index_html_full_path = os.path.join(abs_dirpath, 'index.html')

            # Create the dictionary for this folder
            folder_info = {
                'folder_name': folder_name,
                'parent_folder_path': parent_path,
                'folder_full_path': abs_dirpath,
                'index_html_path': index_html_full_path,
                # You could add relative paths too if needed:
                # 'relative_folder_path': os.path.relpath(abs_dirpath, abs_root_dir)
            }
            folders_with_index.append(folder_info)

        # We don't need to modify 'dirnames'. os.walk will continue into
        # subdirectories regardless. If a subdirectory doesn't have
        # 'index.html', it simply won't be added to our list in a
        # subsequent iteration of the loop.

    return folders_with_index

# --- Example Usage ---

# 1. Define the root folder name you want to scan
start_folder = 'assets/html'

# 2. --- Create a dummy directory structure for demonstration ---
#    (This part is just to make the example runnable without
#     you needing to create the folders manually)
print(f"Setting up a dummy directory structure under '{start_folder}'...")
if os.path.exists(start_folder):
    # Clean up previous runs if necessary
    import shutil
    try:
        shutil.rmtree(start_folder)
    except OSError as e:
        print(f"Error removing old directory: {e}")

# Create root folder with index.html
os.makedirs(start_folder, exist_ok=True)
with open(os.path.join(start_folder, 'index.html'), 'w') as f:
    f.write('<h1>Root Index</h1>')

# Create subfolder with index.html
os.makedirs(os.path.join(start_folder, 'about'), exist_ok=True)
with open(os.path.join(start_folder, 'about', 'index.html'), 'w') as f:
    f.write('<h1>About Index</h1>')

# Create subfolder WITHOUT index.html (should be skipped in the map)
os.makedirs(os.path.join(start_folder, 'products'), exist_ok=True)
with open(os.path.join(start_folder, 'products', 'product1.html'), 'w') as f:
    f.write('<h1>Product 1</h1>') # Not an index.html

# Create a nested subfolder (inside 'products') WITH index.html (should be included)
os.makedirs(os.path.join(start_folder, 'products', 'details'), exist_ok=True)
with open(os.path.join(start_folder, 'products', 'details', 'index.html'), 'w') as f:
    f.write('<h1>Details Index</h1>')

# Create another subfolder without index.html
os.makedirs(os.path.join(start_folder, 'contact'), exist_ok=True)
print("Dummy structure created.")
print("-" * 30)
# --- End of dummy structure creation ---

# 3. Run the function to get the map
print(f"Scanning '{start_folder}' for folders with 'index.html'...")
result_map = find_folders_with_index(start_folder)

# 4. Print the result in a readable format
if result_map is not None:
    print("\nResulting Map (List of Dictionaries):")
    # Use json.dumps for pretty printing the list of dictionaries
    print(json.dumps(result_map, indent=4))

    if not result_map:
        print("No folders containing 'index.html' were found.")
else:
    print(f"Could not process the directory '{start_folder}'. Please check the path and permissions.")

# Optional: Clean up the dummy directory after running
# import shutil
# print(f"\nCleaning up dummy directory '{start_folder}'...")
# try:
#     shutil.rmtree(start_folder)
#     print("Cleanup complete.")
# except OSError as e:
#     print(f"Error during cleanup: {e}")