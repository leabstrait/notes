import os

def generate_collapsible_index(root_dir, skip_list=None):
    index_content = ""

    # Recursive function to generate index content
    def generate_index_recursive(dir_path, depth=0):
        nonlocal index_content
        markdown_files = [f for f in os.listdir(dir_path) if f.endswith(".md")]
        if markdown_files:
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if skip_list and (item in skip_list or item_path in skip_list):
                    continue  # Skip items in the skip list
                if os.path.isdir(item_path):
                    # Create a collapsible section for directories
                    index_content += f"<details><summary>{item}</summary>\n"
                    generate_index_recursive(item_path, depth + 1)
                    index_content += "</details>\n"
                elif item.endswith(".md"):
                    # Convert backslashes to forward slashes for Markdown links
                    relative_path = os.path.relpath(item_path, root_dir).replace("\\", "/")
                    # Remove the .md extension from the file name
                    file_name = os.path.splitext(item)[0]
                    # Create a Markdown link to the file without the .md extension
                    index_content += f"[{file_name}]({relative_path[:-3]})\n"

    # Start generating index content
    generate_index_recursive(root_dir)

    # Write the index content to index.md
    with open(os.path.join(root_dir, "index.html"), "w") as index_file:
        index_file.write(index_content)

# Example usage: Generate collapsible index for the "content" directory, skipping specific files and directories
generate_collapsible_index(".", skip_list=[".git", "CNAME", "genindex.py", "notes.sh"])
