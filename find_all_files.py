import os
import sys

def find_all_files_relative(start_dir, project_root):
    """
    Recursively finds ALL files within a directory and returns their paths
    relative to the project root, using forward slashes.

    Args:
        start_dir (str): The absolute path to the directory to start searching from.
        project_root (str): The absolute path to the Flutter project root.

    Returns:
        list: A list of relative paths (using '/') to all found files.
              Returns an empty list if the start_dir doesn't exist or
              is not a directory.
    """
    all_file_paths_relative = []

    if not os.path.isdir(start_dir):
        print(f"Warning: Asset directory '{start_dir}' not found or is not a directory.")
        return all_file_paths_relative

    for dirpath, dirnames, filenames in os.walk(start_dir):
        for filename in filenames:
            # No extension check needed - we want all files
            full_path = os.path.abspath(os.path.join(dirpath, filename))
            # Calculate path relative to the project root
            relative_path = os.path.relpath(full_path, project_root)
            # Ensure forward slashes for pubspec.yaml
            relative_path_unix = relative_path.replace(os.sep, '/')
            all_file_paths_relative.append(relative_path_unix)

    return all_file_paths_relative

def update_pubspec_assets(pubspec_path, new_assets):
    """
    Updates the pubspec.yaml file to include new asset paths.
    (This function remains the same as the previous version)

    Args:
        pubspec_path (str): The path to the pubspec.yaml file.
        new_assets (list): A list of relative asset paths (strings) to add.

    Returns:
        tuple: (int, int) - Number of assets added, number of assets already present.
               Returns (-1, -1) on error.
    """
    if not os.path.isfile(pubspec_path):
        print(f"Error: '{pubspec_path}' not found.")
        return -1, -1

    try:
        with open(pubspec_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading '{pubspec_path}': {e}")
        return -1, -1

    flutter_section_index = -1
    assets_section_index = -1
    assets_indentation = ""
    existing_assets = set()
    in_assets_section = False
    asset_line_prefix = "" # To store indentation + '- '

    # --- Locate flutter: and assets: sections ---
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        leading_spaces = len(line) - len(line.lstrip(' '))

        if stripped_line.startswith('flutter:'):
            flutter_section_index = i
            continue

        if flutter_section_index != -1 and assets_section_index == -1 and \
           stripped_line.startswith('assets:') and not stripped_line.startswith('#'):
             assets_section_index = i
             assets_indentation = " " * (leading_spaces + 2)
             asset_line_prefix = f"{assets_indentation}- "
             in_assets_section = True
             continue

        if in_assets_section:
            if not line.strip() or leading_spaces < len(assets_indentation):
                 in_assets_section = False
                 continue
            if stripped_line.startswith('-'):
                 asset_path = stripped_line[1:].strip()
                 if asset_path:
                     existing_assets.add(asset_path)

    # --- Prepare new lines ---
    assets_added_count = 0
    assets_present_count = 0
    lines_to_add = []

    for asset in sorted(new_assets): # Sort for consistent order
        if asset not in existing_assets:
            lines_to_add.append(f"{asset_line_prefix}{asset}\n")
            assets_added_count += 1
        else:
            assets_present_count += 1

    if not lines_to_add:
        print("No new assets found to add (all found files might already be listed).")
        return assets_added_count, assets_present_count

    # --- Construct the new file content ---
    new_lines = []
    inserted = False

    if flutter_section_index == -1:
        print("Warning: 'flutter:' section not found. Appending basic structure.")
        new_lines = lines
        new_lines.append("\nflutter:\n")
        new_lines.append("  uses-material-design: true # Example, adjust as needed\n")
        new_lines.append("  assets:\n")
        # Need to determine prefix here for the first time
        asset_line_prefix = "    - " # Assuming 4 spaces for assets under flutter
        lines_to_add_reformatted = [f"{asset_line_prefix}{asset.strip()}\n" for asset in new_assets if asset not in existing_assets]
        new_lines.extend(lines_to_add_reformatted)
        inserted = True
    elif assets_section_index == -1:
        print("Adding 'assets:' section under 'flutter:'.")
        insert_point = flutter_section_index + 1
        flutter_indent = len(lines[flutter_section_index]) - len(lines[flutter_section_index].lstrip(' '))
        assets_section_indent = " " * (flutter_indent + 2)
        asset_line_prefix = f"{assets_section_indent}  - "
        lines_to_add_reformatted = [f"{asset_line_prefix}{asset.strip()}\n" for asset in new_assets if asset not in existing_assets]

        new_lines.extend(lines[:insert_point])
        new_lines.append(f"{assets_section_indent}assets:\n")
        new_lines.extend(lines_to_add_reformatted)
        new_lines.extend(lines[insert_point:])
        inserted = True
    else:
        print(f"Adding assets under existing 'assets:' section (line {assets_section_index + 1}).")
        end_of_assets_index = assets_section_index + 1
        indent_level = len(asset_line_prefix.rstrip('- '))
        while end_of_assets_index < len(lines):
            line = lines[end_of_assets_index]
            leading_spaces = len(line) - len(line.lstrip(' '))
            if not line.strip() or leading_spaces < indent_level:
                 break
            if line.strip().startswith('-') or \
               (line.strip().startswith('#') and leading_spaces >= indent_level) or \
               not line.strip():
                 end_of_assets_index += 1
            else:
                break

        new_lines.extend(lines[:end_of_assets_index])
        # Ensure lines_to_add uses the correctly detected prefix
        lines_to_add_reformatted = [f"{asset_line_prefix}{asset.strip()}\n" for asset in sorted(new_assets) if asset not in existing_assets]
        new_lines.extend(lines_to_add_reformatted)
        new_lines.extend(lines[end_of_assets_index:])
        inserted = True

    if not inserted:
        print("Error: Could not determine where to insert assets. No changes made.")
        return -1, -1

    # --- Write the updated content back ---
    try:
        with open(pubspec_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Successfully updated '{pubspec_path}'")
        return assets_added_count, assets_present_count
    except Exception as e:
        print(f"Error writing updated '{pubspec_path}': {e}")
        return -1, -1

# --- Main Execution ---
if __name__ == "__main__":
    # IMPORTANT: Change this to the folder containing ALL files you want to add
    asset_folder_name = 'assets/html'  # <<< e.g., 'assets', 'static', 'resources', 'html'

    pubspec_filename = 'pubspec.yaml'

    # Assume script is run from the project root
    project_root_dir = os.path.abspath(os.getcwd())
    asset_search_dir = os.path.join(project_root_dir, asset_folder_name)
    pubspec_file_path = os.path.join(project_root_dir, pubspec_filename)

    print(f"Project Root: {project_root_dir}")
    print(f"Searching for ALL files in: {asset_search_dir}")
    print(f"Target Pubspec: {pubspec_file_path}")
    print("-" * 20)

    # 1. Find all files relative to project root
    all_assets = find_all_files_relative(asset_search_dir, project_root_dir)

    if not all_assets:
        print("No files found in the specified asset folder.")
        sys.exit(0) # Exit cleanly, nothing to do

    print(f"Found {len(all_assets)} files.")
    # It might be too many to list, so commenting this out by default:
    # print("Found the following files:")
    # for asset_path in all_assets:
    #     print(f"  - {asset_path}")

    # 2. Update pubspec.yaml
    added, present = update_pubspec_assets(pubspec_file_path, all_assets)

    print("-" * 20)
    if added > -1:
        print(f"Summary: Added {added} new asset paths, {present} were already listed.")
        # Remind user to check!
        print("\nIMPORTANT: Please review pubspec.yaml to ensure only intended files were added.")
    else:
        print("An error occurred during the update process.")
        sys.exit(1) # Exit with error code