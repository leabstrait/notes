# The notes function is used to create and edit notes.
# Notes are stored in a directory called notes.
# The notes directory should be in the home directory.
notes() {
    local notes_dir="$HOME/notes"

    if [[ ! -d "$notes_dir" ]]; then
        echo "Notes directory not found: $notes_dir"
        return 1
    fi

    # check if cwd is notes dir, else cd to it and start from there
    if [[ ! "$PWD" == "$notes_dir"* ]]; then
        echo "Current directory is not $notes_dir"
        cd "$notes_dir"
        echo "Changed directory to $notes_dir"
        notes "$@"
        return $?
    fi

    if [[ "$1" == "create" ]]; then
        if [[ -z "$2" ]]; then
            echo "Usage: notes create <note_name>"
            return 1
        fi

        local full_path="$2"
        local note_name=$(basename "$full_path")
        local note_dir=$(dirname "$full_path")
        mkdir -p $note_dir
        local note_filename="$note_name.md"
        local title_case=$(echo "$note_name" | sed 's/\b\(.\)/\u\1/g' | sed 's/-/ /g')
        local note_path="$notes_dir/$note_dir/$note_filename"
        echo $note_path

        if [[ -e "$note_path" ]]; then
            echo "Note already exists: $title_case"
            return 1
        fi

        # Metadata
        cat <<EOF >"$note_path"
---
title: $title_case
subtitle:
author: Labin Ojha
keywords:
bibliography:
csl: https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl
fontsize: 11.5pt
mainfont: Arial, Palatino, Georgia, Times
---

# $title_case
---
EOF

        echo "Created new note: $title_case"

        "$EDITOR" "$note_path"

    elif [[ "$1" == "edit" ]]; then
        if [[ -z "$2" ]]; then
            echo "Usage: notes edit <note_name>"
            return 1
        fi

        local full_path="$2"
        local note_name=$(basename "$full_path")
        local note_dir=$(dirname "$full_path")
        local note_filename="$note_name.md"
        local note_path="$notes_dir/$note_dir/$note_filename"

        if [[ ! -e "$note_path" ]]; then
            echo "Note not found: $note_name"
            return 1
        fi

        "$EDITOR" "$note_path"
    else
        echo "Usage: notes <create|edit> <note_name>"
        return 1
    fi
}
