---
title: Pass Cheatsheet
keywords:
bibliography:
csl: https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl
---

### `pass` Password Manager Cheatsheet

#### Installation

-   **Archlinux**: `sudo pacman -S pass`

#### Initialization

-   `pass init <gpg-id>`: Initializes Pass with your GPG key.
-   `pass git init`: Initializes Pass to use Git for version control.

#### Adding Passwords

-   `pass insert <path/to/password>`: Adds a new password.
-   `pass insert -m <path/to/password>`: Adds a new multiline password.
-   `pass generate <path/to/password> <length>`: Generates a random password of specified length.
-   `pass generate -c <path/to/password> <length>`: Generates a random password of specified length and copies it to the clipboard.
-   `pass edit <path/to/password>`: Edits an existing password.

#### Viewing Passwords

-   `pass`: Lists all password entries.
-   `pass <path/to/password>`: Displays the password for the specified entry.
-   `pass show -c <path/to/password>`: Copies the password to the clipboard.

#### Sharing and Collaboration

-   `pass git push`: Pushes changes to the Git remote repository.
-   `pass git pull`: Pulls changes from the Git remote repository.
-   `pass git remote add origin <remote-url>`: Sets up a remote repository for syncing.

#### Search and Navigation

-   `pass search <keyword>`: Searches for a password entry containing the specified keyword.
-   `pass find <path>`: Finds passwords matching a specific path.
-   `pass grep <pattern>`: Searches for a pattern within password entries.

#### Managing Passwords

-   `pass cp <old-path> <new-path>`: Copies a password entry to a new location.
-   `pass mv <old-path> <new-path>`: Moves a password entry to a new location.
-   `pass rm <path/to/password>`: Deletes a password entry.
-   `pass rename <old-path> <new-path>`: Renames a password entry.

#### Security

-   Always use strong, unique GPG keys for encryption.
-   Regularly backup your password store.
-   Avoid sharing your GPG private key.

#### Advanced Usage

-   `pass git log <path/to/password>`: Shows the history of changes for a password entry.
-   `pass git checkout <commit> <path/to/password>`: Restores a password entry to a specific version.
