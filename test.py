import os

# Define the directory to search
directory_to_search = 'C:/WorkspaceGIT/Way2WarrenBuffett/Way2WarrenBuffett'  # Replace with the target directory

# Define the file to exclude
excluded_file = 'main_old.py'

# Define the file to write the contents to
output_file = 'common.py'

# Initialize an empty list to hold the file contents
all_file_contents = []

# Walk through the directory
for root, dirs, files in os.walk(directory_to_search):
    for file in files:
        if file.endswith('.py') and file != excluded_file:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                file_contents = f.read()
                # Add the filename and its contents to the list
                all_file_contents.append(f"# {file}\n{file_contents}")

# Write the collected contents to the output file
with open(output_file, 'w') as f:
    for content in all_file_contents:
        f.write(content)
        f.write('\n\n')  # Add some space between files for readability

print(f"Contents of all Python files (excluding {excluded_file}) have been written to {output_file}.")