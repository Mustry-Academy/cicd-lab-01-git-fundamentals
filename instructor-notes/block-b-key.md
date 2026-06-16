# Block B — instructor answer key

> **Do not read this before you've attempted the You-do solo.** The graph drawings in Part 2 are the whole point — if you peek, you won't notice the structural difference between FF and `--no-ff`.

## The seed state

`scripts/seed-messy-state.sh` should drop these three changes into the working tree:

1. **`sample-app/app.py`** — add a docstring to the `greet()` function.
2. **`sample-app/README.md`** — add a "Run me" section with the python command.
3. **`sample-app/tests/test_app.py`** — add a second test, `test_greet_handles_empty_string`.

Three files, three distinct logical changes. `git add -p` will offer each as a separate hunk.

## Part 1 — three clean commits

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

## Part 2 — merge style comparison

After Part 2, both merge styles should be visible in the reflog. The expected graphs:

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

## Part 3 — linear rebase

After Part 3, `git log --graph --decorate --oneline --all` should show a **linear** history:

```
* (HEAD -> main, feature/greeting-tweaks) test: cover empty-string input
* docs: document how to run the sample app
* refactor(app): add docstring to greet()
* main: add README note before merge
* (BASE) <earlier commits>
```

No merge commit. No diverging branch. `main` and `feature/greeting-tweaks` point to the same commit.

The feature commits will have **new SHAs** because rebase rewrites them. Students who don't notice this is a good moment to revisit the "commits are immutable" point — `git rebase` doesn't *move* commits, it creates new ones and re-points the branch.

## Stretch — conflict resolution

The expected conflict:

```
<<<<<<< HEAD
"""Sample app for the Git fundamentals lab."""
# CONFLICT BAIT
=======
"""Sample app for the Git fundamentals lab."""


def greet(name: str) -> str:
    """Return a friendly greeting for `name`."""
=======
>>>>>>> refactor(app): add docstring to greet()
```

(Exact markers will depend on the conflict layout — the structure above is illustrative.)

Resolution: combine the docstring change with the `# CONFLICT BAIT` line. Save, `git add sample-app/app.py`, `git rebase --continue`. The remaining two commits should apply cleanly.

If a student gets stuck, `git rebase --abort` is a legitimate exit — better to bail and try again than to mash through and produce broken history.

## Debrief crib

Use these as conversational threads, not as questions to grade:

- **Merge vs rebase:** rebase produces clean history but loses "this was a branch" signal; merge with `--no-ff` preserves the branch shape but adds noise. Most teams pick one as default. Many shops rebase feature branches and merge with `--no-ff` at PR time.
- **Aliases:** common ones — `lg` for `log --graph --decorate --oneline --all`, `st` for `status -sb`, `co` for `checkout`. Discourage `git unstage` aliases that wrap `reset HEAD --` until students understand the index.
- **Recovery from push-to-main:** the answer depends on whether anyone has pulled yet. If not, `git reset` + `git push --force-with-lease`. If yes, a **revert** is safer — the wrong commit stays in history, but a new commit undoes it. We talk about force-pushing nuance in Lab 02.
