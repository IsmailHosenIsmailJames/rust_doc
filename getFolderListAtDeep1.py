import os

def save_top_level_folders(folder_path, output_file):
    """
    Saves a list of top-level folders (without subfolders) to a text file.

    Args:
        folder_path (str): The path to the folder containing the folders.
        output_file (str): The name of the text file to create.
    """

    top_level_folders = [
        folder for folder in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, folder))
    ]

    with open(output_file, 'w') as f:
        for folder in top_level_folders:
            f.write(folder + '\n')

# Example usage:
folder_path = 'assets/std'  # Replace with the actual folder path
output_file = 'top_level_folders.txt'
save_top_level_folders(folder_path, output_file)

print("Top-level folders saved to:", output_file)
