# Block A — instructor answer key

> **Do not read this before you've attempted the You-do solo.** The whole point of Block A's spelunking is to build intuition; if you skip the discovery you'll skip the learning.

## Pre-requisite: the seeded history

`main` should ship with at least the following commit history. SHAs will differ per-build because Git timestamps are per-author/date, so the key works by **commit messages and `-S` queries**, not literal SHAs.

Recommended seed history (oldest → newest):

1. `chore: initial commit — empty sample-app skeleton`
2. `feat: add greet() function in app.py`
3. `test: cover greet() with a single pytest case`
4. `docs: write sample-app/README.md`
5. `feat: support custom name via argv in __main__`

That gives a 5-commit history with at least two files added, one file expanded, and one feature-style commit that the You-do question #2 can locate via `git log -S "def greet"`.

## You-do answers

### 1. Blob SHA at `HEAD~2`

```bash
git ls-tree HEAD~2 sample-app/app.py
# Expected output (SHA will differ): 100644 blob <BLOB-SHA> sample-app/app.py
git cat-file -p <BLOB-SHA>
# Should print the contents of app.py *as of* HEAD~2 — at that point, the __main__ block doesn't take argv.
git show HEAD~2:sample-app/app.py
# Should match exactly.
```

Common confusion: students sometimes use `HEAD~2` thinking it means "two commits ago including HEAD." It means **the commit two before HEAD** (so HEAD~0 = HEAD, HEAD~1 = previous, HEAD~2 = two back).

### 2. Which commit introduced `greet()`?

```bash
git log -S "def greet" --oneline -- sample-app/app.py
# Should return exactly one commit: the one whose message reads
# "feat: add greet() function in app.py"
```

If the student gets more than one commit, they either:
- Forgot to restrict to `-- sample-app/app.py`, or
- Are sitting on a state where `def greet` has been edited later (rare in the seeded history).

### 3. Tree shape at `HEAD~1`

```bash
git cat-file -p HEAD~1
# Read the tree SHA from this output.
git cat-file -p <TREE-SHA>
# Lists top-level entries — should be: sample-app (tree), and the lab-level files.
git ls-tree -r --name-only HEAD~1
# Recursive list — at HEAD~1 (i.e., before the final argv feature), expect:
#   sample-app/README.md
#   sample-app/app.py
#   sample-app/requirements.txt
#   sample-app/tests/test_app.py
# (plus any lab-level files like README.md, .gitignore, etc.)
```

The exact file count depends on what else is committed at the lab level on `main`. The `verify-block-a.sh` script handles this.

### 4. Make a focused commit

Expected diff in the new commit: exactly one hunk in `sample-app/README.md` adding a "lab participant" line.

```bash
git cat-file -p HEAD
# tree <TREE-SHA>
# parent <PARENT-SHA>
# author …
# committer …
#
# <commit message>
git cat-file -p <TREE-SHA>
# Should show sample-app/ entry pointing to a *changed* sub-tree.
git ls-tree HEAD sample-app/
# README.md blob SHA should differ from HEAD~1's README.md blob SHA.
# All other blob SHAs (app.py, requirements.txt, tests/) should be UNCHANGED.
```

Common mistake: students accidentally also save unrelated file changes (e.g., they ran `pytest` and a `.pytest_cache/` got pulled in). The `.gitignore` covers `.pytest_cache/`, but if they forced an add, you'll see additional blobs. Look for `git add .` in their shell history.

## Stretch challenge — reconstructing `git diff`

Reference walk-through for the stretch:

```bash
# Pick two adjacent commits, say HEAD and HEAD~1.
git ls-tree -r HEAD       > /tmp/tree-head.txt
git ls-tree -r HEAD~1     > /tmp/tree-prev.txt
diff /tmp/tree-prev.txt /tmp/tree-head.txt
# Lines that appear only in tree-head.txt → added or modified files
# Lines that appear only in tree-prev.txt → removed or modified files
# (matched on path; the SHA difference tells you the blob changed)

# For a changed file:
git cat-file -p <OLD-BLOB-SHA>  > /tmp/old.txt
git cat-file -p <NEW-BLOB-SHA>  > /tmp/new.txt
diff /tmp/old.txt /tmp/new.txt
# This output matches what `git diff HEAD~1 HEAD -- <path>` shows (minus the header).
```

Goal of the stretch: students see that `git diff` is not a black box — it's a tree walk + blob comparison. The mental model from Block A's first half is now operational.
