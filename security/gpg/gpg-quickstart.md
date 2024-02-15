---
title: GPG Quickstart
keywords:
bibliography:
csl: https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl
---

## GPG (GNU Privacy Guard) Quick Start

### Installation and Setup:

-   #### Install GnuPG on Archlinux

    ```bash
    sudo pacman -S gnupg
    ```

-   #### Adjust Permissions for GPG Home Directory:

    ```bash
    chmod 0700 ~/.gnupg/
    ```

-   #### Customize GPG Home Directory (Optional):
    ```bash
    export GNUPGHOME=/tmp/gnupg
    ```

### Key Management

-   #### Check Existing Keys:

    ```bash
    gpg --list-keys
    ```

-   #### Generate New Key Pair:

    ```bash
    gpg --full-generate-key
    ```

-   #### Generating a Key Pair with Specific Expiry Date:

    ```bash
    gpg --full-generate-key --expire-date YYYY-MM-DD
    ```

-   #### Generating a Key Pair with Specific Parameters:

    ```bash
    gpg --full-generate-key --default-key-algo rsa4096
    ```

-   #### Managing Subkeys:

    -   List subkeys:
        ```bash
        gpg --list-secret-keys --with-subkey-fingerprints
        ```
    -   Add subkey:
        ```bash
        gpg --edit-key email@example.com
        addkey
        ```

-   #### Update Key Expiration Date:

    -   Changing Expiry Date:
        ```bash
        gpg --edit-key email@example.com
        expire
        ```

-   #### Adding or Changing Passphrase:

    ```bash
    gpg --edit-key email@example.com
    passwd
    ```

-   #### Create Revoke Certificate (GnuPG < 2.1):

    ```bash
    gpg --output revoke-email@example.asc --gen-revoke email@example.com

    # Revoke the key with this revoke certificate generated above
    gpg --import revoke-email@example.asc
    ```

-   #### Revoking a Key:

    ```bash
    gpg --edit-key email@example.com
    revkey
    ```

-   #### Setting Key Trust Level:
    ```bash
    gpg --edit-key email@example.com
    trust
    ```
-   #### Removing a key from the public keyring

    ```bash
    gpg --delete-keys user@example.com
    ```

-   #### Removing a key from the secret keyring
     !! UNSAFE, BE CAREFUL !!

    ```bash
    gpg --delete-secret-keys user@example.com
    ```

### Searching, Importing and Exporting GPG Keys

-   #### Searching for a GPG Key on a Keyserver:

    ```bash
    gpg --search-keys user@example.com
    ```

-   #### Importing a GPG Key from a Keyserver:

    ```bash
    gpg --recv-keys KEY_ID
    ```

-   #### Export Public Key to file:

    ```bash
    gpg --export --armor email@example.com > public_key.gpg
    gpg --export --armor --output email@example.gpg.pub email@example.com
    ```

-   #### Exporting Your Public GPG Key to Send to Another User:

    ```bash
    gpg --export --armor --output your_public_key.gpg YOUR_EMAIL
    ```

-   #### Sending Your Public GPG Key to a Keyserver:

    ```bash
    gpg --list-keys --keyid-format LONG YOUR_GPG_EMAIL
    gpg --send-keys YOUR_KEY_ID_FROM_ABOVE
    ```

-   #### Importing Another User's Public GPG Key from a File:

    ```bash
    gpg --import their_public_key.gpg
    ```

-   #### Exporting Private Key to file:

    ```bash
    gpg --export-secret-keys --armor email@example.com > private_key.asc
    ```

-   #### Importing Private Key from file:

    ```bash
    gpg --import private_key.asc
    ```

### Encrypting and Decrypting Files

-   #### Encrypting a File:

    ```bash
    gpg --encrypt --recipient recipient@email.com file.txt
    ```

-   #### Decrypting a File:

    ```bash
    gpg --decrypt file.txt.gpg > decrypted_file.txt
    ```

-   #### Encrypting and Decrypting Files with Symmetric Encryption:

    -   Encrypting:
        ```bash
        gpg --symmetric file.txt
        ```
    -   Decrypting:
        ```bash
        gpg --decrypt file.txt.gpg
        ```

-   #### Encrypting for Multiple Recipients:

    ```bash
    gpg --encrypt --recipient email1@example.com --recipient email2@example.com file.txt
    ```

-   #### Encrypting a File with Multiple Passphrases:

    ```bash
    gpg --symmetric --cipher-algo AES256 --recipient email1@example.com --recipient email2@example.com file.txt
    ```

-   #### Encrypting and Signing Messages:

    ```bash
    gpg --sign --encrypt --armor --recipient email@example.com file.txt
    ```

-   #### Decrypting a File and Verifying Signature:

    ```bash
    gpg --decrypt file.txt.gpg | gpg --verify file.txt.sig
    ```

-   #### Generating a Random Password with GPG:

    ```bash
    gpg --gen-random --armor 1 12
    ```

### Signing and Verifying

-   #### Signing a File:

    ```bash
    gpg --sign file.txt
    ```

-   #### Verifying a Signature:
    ```bash
    gpg --verify file.txt.sig
    ```

### Configuration

-   #### Setting Preferences for Keyserver:
    ```bash
    nano ~/.gnupg/gpg.conf
    # Add/edit the line:
    # keyserver hkps://keys.openpgp.org
    ```

### Key Backups :

-   Regularly back up both public and private keys to prevent loss.
-   Backup entire directory: `cp -r ~/.gnupg/ /path/to/backup/location`
-   Backup private key only: `gpg --export-secret-keys --output email@example.gpg --armor email@example.com`
