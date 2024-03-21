import os

root_dir = os.getcwd()
readme_path = os.path.join(root_dir, "README.md")
readme_content = ""

def contains_md_files(enter_dir):
    """Check if the directory contains Markdown files."""
    for item in os.listdir(enter_dir):
        item_path = os.path.join(enter_dir, item)
        if os.path.isdir(item_path):
            if contains_md_files(item_path):
                return True
        elif item.endswith(".md"):
            return True
    return False

def traverse(enter_dir, skip_list=None):
    """Traverse the directory tree and add Markdown files to the README."""
    global readme_content
    for item in sorted(os.listdir(enter_dir)):
        if skip_list and item in skip_list:
            continue
        item_path = os.path.join(enter_dir, item)
        if os.path.isdir(item_path):
            if contains_md_files(item_path):
                readme_content += f"\n### {item}\n"
            traverse(item_path, skip_list)
        elif item.endswith(".md"):
            relative_path = os.path.relpath(item_path, root_dir)
            readme_content += f"  - [{item.replace('.md', '')}]({relative_path})\n"

# Call the traverse function to update readme_content
traverse(root_dir, skip_list=[".git", "CNAME", "gen_readme.py", "README.md"])

# Write the content to README.md
with open(readme_path, "w") as readme_file:
    readme_file.write(readme_content)

print(f"README.md updated with the file list from {root_dir}")
