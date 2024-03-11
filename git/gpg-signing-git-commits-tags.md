# GPG Signing git Commits Tags

### Signing and Verifying git Commits on the Command Line and GitHub

A GPG key-pair is required for the following:

#### Signing Commits and Tags

-   **Signing a Commit:**

    ```bash
    git commit -S -m "Commit message"
    ```

-   **Signing a Tag:**
    ```bash
    git tag -sm "Tag message" tag_name
    ```

#### Auto-signing Configuration

-   **Configuring git to Auto-sign Commits and Tags:**
    ```bash
    git config --global commit.gpgsign true
    git config --global tag.gpgsign true
    ```

#### Verifying Commits and Tags

-   **Verifying Signed Commits:**

    ```bash
    git log --show-signature
    ```

-   **Verifying Signed Tags:**
    ```bash
    git tag -v tag_name
    ```

#### Branch Protection and Verification

-   **Verifying Signatures when Merging a Branch with Git:**

    ```bash
    git merge --verify-signatures -S feature-branch # -S is to sign the merge commit, which is automatic if [commit] gpgsign=true is set in .gitconfig
    ```

-   **Enforcing Signed Commits on GitHub:**
    -   Go to repository Settings -> Branches -> Branch Protection rules and add a rule to require signed commits.
