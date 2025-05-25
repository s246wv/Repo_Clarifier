import os
import sys

def read_directory_structure(startpath):
    """
    Reads the directory structure starting from startpath and returns it as a string.
    """
    output = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        output.append('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            output.append('{}{}'.format(subindent, f))
    return '\n'.join(output)

if __name__ == '__main__':
    # Read the directory structure of a directory specified as a command-line argument
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        # Use current directory if no argument is provided
        print("No directory path provided as an argument. Using the current directory.")

        target_dir = "."  # Use current directory if no path is provided

    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
    else:
        structure = read_directory_structure(target_dir)
    print(structure)
