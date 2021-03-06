#!/usr/bin/env python

import os
import subprocess


def convert_tex_to_html(directory, entry):
    output_filename = entry.replace(".tex", ".html")
    output_path = os.path.abspath(
        os.path.join("docs", os.path.relpath(directory, os.getcwd()), output_filename)
    )
    print(output_path)
    command = ["pandoc", "--citeproc", entry, "-s", "-o", output_path]
    # change working directory to the one containing the source tex files so that all relative references
    # work, and also so that we don't need to construct absolute paths of the documents we are processing
    # the output path will still be an absolute path
    subprocess.run(command, cwd=directory, check=True)

def convert_html_to_html(directory, entry, title, files_and_folders):
    # output_filename = entry
    # output_path = os.path.abspath(
    #     os.path.join("docs", os.path.relpath(directory, os.getcwd()), output_filename)
    # )
    # print(output_path)
    command = [
        "pandoc",
        "--citeproc",
        "--metadata",
        f"title={title}",
        "--metadata",
        f"keywords={', '.join(files_and_folders)}",
        entry,
        "-s",
        "-o",
        entry
    ]
    # change working directory to the one containing the source tex files so that all relative references
    # work, and also so that we don't need to construct absolute paths of the documents we are processing
    # the output path will still be an absolute path
    subprocess.run(command, cwd=directory, check=True)

def convert_md_to_html(directory, entry):
    output_filename = entry.replace(".md", ".html")
    output_path = os.path.abspath(
        os.path.join("docs", os.path.relpath(directory, os.getcwd()), output_filename)
    )
    print(output_path)
    command = ["pandoc", "--citeproc", entry, "-s", "-o", output_path]
    # change working directory to the one containing the source md files so that all relative references
    # work, and also so that we don't need to construct absolute paths of the documents we are processing
    # the output path will still be an absolute path
    subprocess.run(command, cwd=directory, check=True)


def copy_as_is(directory, entry):
    output_path = os.path.abspath(
        os.path.join("docs", os.path.relpath(directory, os.getcwd()), entry)
    )
    print(output_path)
    command = ["cp", entry, output_path]
    # change working directory to the one containing the source files so that all relative references
    # work, and also so that we don't need to construct absolute paths of the documents we are processing
    # the output path will still be an absolute path
    subprocess.run(command, cwd=directory, check=True)


def create_index_html(directory):
    files_and_folders = []

    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.name == "gen-html-and-index-recursive.py":
                continue

            if entry.name == "gen-readme-recursive.py":
                continue

            if entry.name == "notes.sh":
                continue

            if entry.name == "references.bib":
                continue

            if entry.name.startswith("."):
                continue

            if entry.name.startswith("docs"):
                continue

            if entry.is_dir():
                subdirectory_path = os.path.join(directory, entry.name)
                os.makedirs(
                    os.path.join(
                        "docs", os.path.relpath(directory, os.getcwd()), entry.name
                    ),
                    exist_ok=True,
                )
                result = create_index_html(subdirectory_path)
                if result:
                    files_and_folders.append(entry.name)
                continue

            if entry.name.endswith(".tex"):
                convert_tex_to_html(directory, entry.name)
                files_and_folders.append(entry.name)
                continue

            if entry.name.endswith(".md"):
                convert_md_to_html(directory, entry.name)
                files_and_folders.append(entry.name)
                continue

            copy_as_is(directory, entry.name)

    if len(files_and_folders) == 0:
        return False

    # Sort files and folders alphabetically
    files_and_folders.sort()

    # Generate the content for index.html
    title = " ".join(os.path.basename(directory).split('-')).capitalize()
    content = ""
    for item in files_and_folders:
        if item.endswith(".tex"):
            item_link = f"{item.replace('.tex', '.html')}"
            content += f"<p> <a href='{item_link}'>{item.replace('.tex', '')}</a> <a href='{item.replace('.tex', '.pdf')}'>PDF 🗎</a></p>\n"
            continue

        if item.endswith(".md"):
            item_link = f"{item.replace('.md', '.html')}"
            content += (
                f"<p> <a href='{item_link}'>{item.replace('.md', '')}</a> </p>\n"
            )
            continue

        item_link = f"{item}/"
        content += f"<p><a href='{item_link}'>{item}</a></p>\n"

    # Write the content to index.html
    index_path = os.path.abspath(
        os.path.join("docs", os.path.relpath(directory, os.getcwd()), "index.html")
    )
    with open(index_path, "w") as index_file:
        index_file.write(content)
    convert_html_to_html(directory, index_path, title, files_and_folders)

    return True


# Start creating index.html and converting files into the 'docs' folder at the root of the project
current_directory = os.getcwd()
docs_directory = os.path.join(current_directory, "docs")
os.makedirs(docs_directory, exist_ok=True)
create_index_html(current_directory)
