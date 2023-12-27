---
title: Rename All Files Folders Specified Pattern
keywords:
csl: https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl
---

```bash
find . -depth -name '*_*' -execdir bash -c 'for f; do mv "$f" "${f//_/-}"; done' bash {} +
```

This command uses a `for` loop within the `execdir` option to iterate over the files and directories found by `find` and performs the renaming using the `mv` command.

Here's a breakdown of the command:

-   `find .`: Searches for files and directories in the current directory and its subdirectories.
-   `-depth`: Processes the directory contents before the directory itself.
-   `-name '*_*'`: Specifies the pattern for filenames and directory names containing underscores.
-   `-execdir bash -c 'for f; do mv "$f" "${f//_/-}"; done' _whatever_ {} +`: For each batch of files or directories found, it executes a bash command that uses a `for` loop to iterate over the items and rename them using the `mv` command.

    -   _Note_: The `_whatever_` is needed because without it `bash` with the `-c` option will ignore the first result of the `find` command in `{}`.
    -   From the `man` page for `bash`:
        ```
        -c string
        If the -c option is present, then commands are read from string. If there are arguments after the string, they are assigned to the positional parameters, starting with $0.
        ```
    -   The `-c` flag in `bash` will execute the command string with the parameters starting from `$1` and not `$0`, as `$0` is the name of the script and not the file-paths being sent to the `bash` `'<command string>'`.
    -   Hence, we fill the `$0` parameter with a dummy argument. It is typically set to `bash` or `_` for clarity.
    -   Study the outputs of these commands to see the difference.
        -   `find . -name '*.md' -execdir bash -c 'echo "$@"' _ {} +`
        -   `find . -name '*.md' -execdir bash -c 'echo "$0"' _ {} +`
        -   `find . -name '*.md' -execdir bash -c 'echo "$@"' {} +`
        -   `find . -name '*.md' -execdir bash -c 'echo "$1"' _ {} +`
        -   `find . -name '*.md' -execdir bash -c 'echo "$1"' {} +`

    See [this stackoverflow answer](https://stackoverflow.com/a/60216452) and [another stackoverflow answer](https://stackoverflow.com/a/38867117) for further clarification.
