---
title: Test Merge
csl: https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl
---


We can use `git merge --no-commit` to prevent the merge from actually being committed, and if we don't like how the merge works out, just reset to the original head. If you definitely don't want to finalize the merge, even if it's a fast-forward (and thus has no conflicts, by definition), you could add `--no-ff` as well.
-   `git config --global alias.merge-test '!f() { git merge --no-commit --no-ff "$@"; echo "Run \"git merge --abort\" if you don'\''t want to commit the changes"; }; f'`

To be more safe, we can do the following:

-   ```bash
      git checkout main
      git checkout -b test-merge
      git merge topic-branch
    ```

    After completing the merge, it is easy to see the consolidated change from main

-   ```bash
      git diff main
    ```

    When done, simply delete the test-merge branch

-   ```bash
      git checkout main
      git branch -D test-merge
    ```

    This way, the main branch never changes.

[Stack Overflow Question - How to test a merge without actually merging first](https://stackoverflow.com/questions/7484199/how-to-test-a-merge-without-actually-merging-first)
