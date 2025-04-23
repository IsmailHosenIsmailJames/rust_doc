import os

def find_html_files(start_dir):
    """
    Recursively finds all files with the '.html' extension within a directory.

    Args:
        start_dir (str): The path to the directory to start searching from.

    Returns:
        list: A list of absolute paths to all found .html files.
              Returns an empty list if the start_dir doesn't exist,
              is not a directory, or no .html files are found.
    """
    html_file_paths = []

    # Ensure the starting directory exists and is actually a directory
    if not os.path.isdir(start_dir):
        print(f"Error: Starting directory '{start_dir}' not found or is not a directory.")
        return html_file_paths # Return empty list

    # os.walk yields a 3-tuple for each directory it visits:
    # dirpath: string, the path to the directory.
    # dirnames: list, the names of the subdirectories in dirpath.
    # filenames: list, the names of the non-directory files in dirpath.
    for dirpath, dirnames, filenames in os.walk(start_dir):
        for filename in filenames:
            # Check if the file extension is '.html' (case-sensitive)
            # Use filename.lower().endswith('.html') for case-insensitive
            if filename.endswith('.html'):
                # Construct the full absolute path
                full_path = os.path.abspath(os.path.join(dirpath, filename))
                html_file_paths.append(full_path)

    return html_file_paths

# --- Main Execution ---
if __name__ == "__main__":
    root_folder_name = 'assets/html'  # The directory to search within

    # Get the absolute path for clarity, even if the script is run from elsewhere
    search_directory = os.path.abspath(root_folder_name)

    print(f"Searching for .html files in: '{search_directory}'...")

    # Call the function to find the files
    all_html_files = find_html_files(search_directory)

    # Print the results
    if all_html_files:
        print("\nFound the following .html files:")
        for file_path in all_html_files:
            print(file_path)

        # Optional: Save the list to a text file
        output_filename = 'html_files_list.txt'
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                for file_path in all_html_files:
                    f.write(file_path + '\n') # Add newline after each path
            print(f"\nList of files saved to '{output_filename}'")
        except IOError as e:
            print(f"\nError writing list to file '{output_filename}': {e}")

    else:
        # Check again if the directory existed, print appropriate message
        if os.path.isdir(search_directory):
            print("\nNo .html files found in the specified directory.")
        # The error for non-existent directory is handled within the function.