# Lab 01 — instructor answer key

> **Do not read this before you've attempted the You-do solo.** The whole point of Phase 1's spelunking is to build intuition, and the graph drawings in Phase 2 are the payoff — if you peek, you'll skip the learning and you won't notice the structural difference between FF and `--no-ff`.

## Pre-requisite: the seeded history

`sample-app/app.py` should have **three** commits in its history (`git log --oneline -- sample-app/app.py`), oldest → newest:

1. **initial commit** — `app.py` is born with `greet()` and an argv-driven `__main__`.
2. **add shout functionality** — `greet()` gains the `shout` parameter / `--shout` flag.
3. **add farewell functionality** — `farewell()` is added alongside `greet()`.

SHAs differ per-build because Git timestamps are per-author/date, so the key works by **commit messages and `-S` queries**, not literal SHAs. The questions are deliberately phrased against `app.py`'s own history (found via `git log -- sample-app/app.py`) rather than `HEAD~N`, so unrelated doc/lab commits stacked on top don't throw off the answers.

## Phase 1 — spelunk + focused commit

### 1. `app.py`'s own history

```bash
git log --oneline -- sample-app/app.py
# Three commits, newest first:
#   <sha> add farewell functionality to sample-app
#   <sha> add shout functionality to the sample application
#   <sha> initial commit
```

Students should pick out the **shout** commit and the **farewell** commit by message — both are reused in #4/#5 and #3.

### 2. Which commit introduced `greet()`?

```bash
git log -S "def greet" --oneline -- sample-app/app.py
# Returns exactly one commit: the INITIAL commit.
```

The "surprise" is that `greet()` has been there since the very first commit — it predates both `shout` and `farewell`. (The `shout` commit edits the `def greet` line but doesn't change the *count* of "def greet", so `-S` doesn't report it.) If a student gets more than one commit, they forgot the `-- sample-app/app.py` pathspec.

### 3. Which commit introduced `farewell()`?

```bash
git log -S "def farewell" --oneline -- sample-app/app.py
# Returns exactly one commit: "add farewell functionality to sample-app".
```

Contrast with #2: `greet()` is original, `farewell()` is a later addition. Same tool (`-S`), two different commits — the point is that `-S` finds *content*, not position.

### 4. Blob SHA before `farewell()` existed

```bash
git ls-tree <shout-SHA> sample-app/app.py
# 100644 blob <BLOB-SHA> sample-app/app.py
git cat-file -p <BLOB-SHA>
# app.py as of the shout commit: greet() with shout support, but NO farewell() yet.
git show <shout-SHA>:sample-app/app.py
# Should match the blob byte-for-byte.
```

Confirm with the student that `farewell()` is absent here — that's the whole point of picking the commit *before* it was added.

### 5. Tree shape at that commit

```bash
git cat-file -p <shout-SHA>
# Read the tree SHA from this output, then:
git cat-file -p <TREE-SHA>
# Top-level entries: sample-app (tree) plus the lab-level files.
git ls-tree -r --name-only <shout-SHA>
# Inside sample-app/, expect exactly four files:
#   sample-app/README.md
#   sample-app/app.py
#   sample-app/requirements.txt
#   sample-app/tests/test_app.py
# (plus whatever lab-level files existed at that commit — count varies by build).
```

The `sample-app/` subtree is the stable part (four files). The lab-level file count depends on what else was committed at that point, so don't grade on the total.

### 6. Make a focused commit

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

### 7. Sanity check

`scripts/verify-lab.sh` should print all-green here. It checks a clean tree, a "lab participant" line in `sample-app/README.md`, and that `HEAD` touched **only** `sample-app/README.md`. Students must run it **before** Phase 2's resets — once Phase 2 rewrites history, the "HEAD touched only README" invariant no longer holds.

## Phase 2 — workflows

### The seed state

`scripts/seed-messy-state.sh` should drop these three changes into the working tree:

1. **`sample-app/app.py`** — add a docstring to the `greet()` function.
2. **`sample-app/README.md`** — add a "Run me" section with the python command.
3. **`sample-app/tests/test_app.py`** — add a second test, `test_greet_handles_empty_string`.

Three files, three distinct logical changes. `git add -p` will offer each as a separate hunk.

### Part A — three clean commits

After `git add -p` and three commits, the expected log on `feature/greeting-tweaks` is:

```
* abc1234 (HEAD -> feature/greeting-tweaks) test: cover empty-string input
* def5678 docs: document how to run the sample app
* 9abcdef refactor(app): add docstring to greet()
* … BASE ancestry below this point
```

The exact commit ordering depends on the student. What matters is:

- **Three commits**, not one or two.
- Each commit touches **exactly one file**.
- Messages are descriptive (not `wip`, `update`, or `stuff`).

If a student lumps everything into a single commit, push them back to redo with `git reset HEAD~1 --soft` and try `add -p` again. The point of `-p` is staging discipline; one giant commit defeats the exercise.

### Part B — merge style comparison

After Part B, both merge styles should be visible in the reflog. The expected graphs:

**Fast-forward attempted (step 7):** at this point `main` has *moved* via the README commit, so a plain `git merge` will **not** fast-forward. Git produces an implicit merge commit:

```
*   merge commit on main
|\
| * test: cover empty-string input
| * docs: document how to run the sample app
| * refactor(app): add docstring to greet()
* | main: add README note before merge
|/
* BASE
```

**`--no-ff` (step 9):** after the reset, `main` is at `BASE` + the README commit. The `--no-ff` merge forces a merge commit even if FF were possible:

```
*   Merge feature/greeting-tweaks-noff into main
|\
| * test: cover empty-string input        (cherry-picked SHAs differ from the original)
| * docs: document how to run the sample app
| * refactor(app): add docstring to greet()
* | main: add README note before merge
|/
* BASE
```

**Key teaching point:** the graphs *look* similar because in both cases `main` has diverged. The distinction that matters is what would happen if `main` *hadn't* moved:

- Plain `merge` would fast-forward (no merge commit, linear history).
- `--no-ff` would still force a merge commit (preserves the "this was a branch" signal).

Demo this explicitly in debrief if students didn't catch it: reset to `BASE`, branch, commit, then merge each way *without* moving `main`.

### Part C — linear rebase

After Part C, `git log --graph --decorate --oneline --all` should show a **linear** history:

```
* (HEAD -> main, feature/greeting-tweaks) test: cover empty-string input
* docs: document how to run the sample app
* refactor(app): add docstring to greet()
* main: add README note before merge
* (BASE) <earlier commits>
```

No merge commit. No diverging branch. `main` and `feature/greeting-tweaks` point to the same commit.

The feature commits will have **new SHAs** because rebase rewrites them. Students who don't notice this is a good moment to revisit the "commits are immutable" point from the I-do — `git rebase` doesn't *move* commits, it creates new ones and re-points the branch.

## Stretch keys

### 1. Reconstructing `git diff`

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

Goal: students see that `git diff` is not a black box — it's a tree walk + blob comparison. The mental model from the I-do is now operational.

### 2. Conflict resolution

Both branches inserted a different line just above `message =` inside `greet()`, so the conflict lands there. During the rebase, `HEAD` is `main` (the comment) and the incoming side is the feature commit (the docstring):

```
def greet(name: str, shout: bool = False) -> str:
<<<<<<< HEAD
    # CONFLICT BAIT — main and your feature branch both edit greet()
=======
    """Return a friendly greeting for `name`."""
>>>>>>> <hash> (refactor(app): add docstring to greet())
    message = f"Hello, {name}!"
```

Resolution: keep **both** lines (delete the three `<<<<<<<` / `=======` / `>>>>>>>` markers, leave the comment and the docstring). Save, `git add sample-app/app.py`, `git rebase --continue`. If a student gets stuck, `git rebase --abort` is a legitimate exit — better to bail and try again than to mash through and produce broken history.

## Debrief crib

Use these as conversational threads, not as questions to grade:

- **Object model in practice:** rebase conflicts, `git reflog` recovery, and "`git mv` is just rename + commit" all make sense once you see commits/trees/blobs. Ask where the model clicked for them during the solo.
- **Merge vs rebase:** rebase produces clean history but loses "this was a branch" signal; merge with `--no-ff` preserves the branch shape but adds noise. Most teams pick one as default. Many shops rebase feature branches and merge with `--no-ff` at PR time.
- **Aliases:** common ones — `lg` for `log --graph --decorate --oneline --all`, `st` for `status -sb`, `co` for `checkout`. Discourage `git unstage` aliases that wrap `reset HEAD --` until students understand the index.
- **Recovery from push-to-main:** the answer depends on whether anyone has pulled yet. If not, `git reset` + `git push --force-with-lease`. If yes, a **revert** is safer — the wrong commit stays in history, but a new commit undoes it. We talk about force-pushing nuance in Lab 02.
