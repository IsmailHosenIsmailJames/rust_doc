import os

def save_file_paths(folder_path, output_file):
    """
    Saves the paths of all files within a folder to a .txt file.

    Args:
        folder_path (str): The path to the folder containing the files.
        output_file (str): The name of the .txt file to create.
    """

    with open(output_file, 'w') as f:
        for root, directories, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                f.write("- "+file_path + '\n')

# Example usage:
folder_path = 'assets'  # Replace with the actual folder path
output_file = 'file_paths.txt'
save_file_paths(folder_path, output_file)

print("File paths saved to:", output_file)
