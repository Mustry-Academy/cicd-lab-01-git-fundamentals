# Lab 01 — Git Fundamentals

**Duration:** ~180 minutes

* 20 min — why version control
* 30 min — the object model, hands-on the workflow
* 20 min — we-do
* 50 min — you-do (solo)
* 15 min — stretch / buffer
* 15 min — debrief

This is one continuous lab. We deliberately blend Git's *object model* with the
*everyday workflow* so that the two reinforce each other: you'll watch `add -p` build the
index, watch a commit produce a fresh tree and blob, and come to see `rebase` as
"new commit objects, not moved ones." The object model isn't an abstract first hour — it's
the lens for every workflow move you make.

## Goal

You should leave this lab able to:

- Articulate **three concrete reasons** version control matters in software work
- Describe what a **commit**, **tree**, and **blob** physically are inside `.git/objects/`
- Use `git cat-file`, `git ls-tree`, and `git log -S` to explore a repository's object graph
- Explain in your own words what HEAD, refs, and the index do
- Stage hunks selectively with `git add -p`
- Use `git switch` and `git switch -c` confidently
- Choose between **merge** (fast-forward vs `--no-ff`) and **rebase** deliberately, and explain the tradeoffs
- Clean up history with `git rebase -i` before review
- Recover from "oh no I committed to the wrong branch"

If you'd like to read ahead: [`docs/why-version-control.md`](../docs/why-version-control.md) and [`docs/git-object-model.md`](../docs/git-object-model.md).

## Pre-flight

```bash
git switch main
git status        # should be clean
chmod +x scripts/seed-messy-state.sh
```

You should see a `sample-app/` directory with several commits already in its history. Run
`git log --oneline` and confirm you see at least five commits, and that the seed script is
available.

## I do — Why version control matters (20 min)

The instructor walks through:

1. **Pre-VC pain.** `FINAL_v2_actual_REAL.zip`, lost work, no audit trail. Anyone who's been in industry long enough has a story.
2. **What a Version Control System (VCS) gives you.** History, blame, branching, safe undo. Show a single `git blame` on `sample-app/app.py` to make the point.
3. **Centralized vs distributed.** Why Git won. Why "every clone is a full backup" matters when the central server is down.
4. **Live folder-vs-repo contrast.** `mkdir scratch && cd scratch && echo hi > a.txt`. Then the same with `git init`. What's tracked? What isn't? What happens when you change `a.txt`?

This segment ends with a one-sentence prompt the group answers around the room: *"What's a version-control disaster you've personally lived through, or watched somebody else live through?"*

## I do — The object model, hands-on the workflow (30 min)

The instructor live-codes, narrating the object graph at every step. The thread: *every
workflow command is really a manipulation of commits, trees, and blobs.*

**1. A commit is a tree.** Walk the existing `sample-app/` history:

1. `git log --oneline` — note one commit's SHA, e.g. `a1b2c3d`.
2. `git cat-file -p a1b2c3d` — read the commit object out loud. Note the `tree` line and the `parent` line.
3. `git cat-file -p <tree-SHA>` — read the tree object. It lists blobs and sub-trees by SHA.
4. `git cat-file -p <blob-SHA>` — see the raw file content.
5. Sketch the commit → tree → blob graph on the board.

Key points: commits point to a *single* tree; trees point to blobs and trees; blobs are *just* content (no filename). The filename lives in the tree entry.

**2. What a commit actually does.** Now make the graph move:

1. Edit one line of `sample-app/README.md`.
2. `git add sample-app/README.md` — explain that the **index** now holds a new blob, staged but not committed. `git status` shows the staged change.
3. `git commit -m "docs: tweak intro"` — a **new commit object** is born, pointing at a **new tree**, whose `README.md` entry points at a **new blob**. `HEAD` (a **ref**) advances to it.
4. `git cat-file -p HEAD`, then its tree, then the README blob — confirm only the README blob SHA changed; `app.py`'s blob is byte-for-byte the same SHA as before. *Unchanged content is never re-stored.*

Land the three moving parts here: **HEAD** (where you are), **refs** (named pointers like `main`), the **index** (the staging area between working tree and the next commit).

**3. Branching and rewriting are just pointer moves and new objects.**

1. `git switch -c demo/throwaway` — a branch is a *cheap pointer* to a commit. Nothing is copied.
2. `git rebase -i HEAD~3` — reorder, squash, reword. Show the commit SHAs **change**: rebase doesn't *move* commits, it **creates new commit objects** and re-points the branch. Tie it straight back to "commits are immutable; their SHA is their content."
3. **Merge — fast-forward.** When `main` hasn't moved, `git merge demo/throwaway` just slides the `main` pointer forward. No merge commit. Linear history.
4. **Merge — `--no-ff`.** Advance `main` with a separate commit, then `git merge --no-ff demo/throwaway`. Now there **is** a merge commit (a commit with *two* parents). The graph shows the branch shape. Display both with `git log --graph --decorate --oneline --all`.
5. **Oops-recovery.** "Oops, committed to main." Demo `git reset HEAD~1 --soft` — the ref moves back one commit but the change stays in the **index** — then `git switch -c feature/recovered && git commit`. Reinforce: `reset` moves a ref; your blobs didn't go anywhere.

## We do (20 min)

Follow along on your own clone.

**Part 1 — trace a commit through the object graph.**

1. Make a small change to `sample-app/README.md` — add a single sentence.
2. `git add sample-app/README.md && git commit -m "docs: expand sample-app intro"`.
3. `git cat-file -p HEAD` — read it out loud. Note the `tree` SHA and the `parent` SHA.
4. `git cat-file -p <tree-SHA>` — find the entry for `README.md`. Note its blob SHA.
5. `git cat-file -p <blob-SHA>` — confirm it matches your new file content.
6. `git ls-tree HEAD sample-app/` — see the tree expressed in one line.

**Part 2 — stage by hunk.** Reset back to a clean tree first: `git reset --hard HEAD~1` (this drops the practice commit above — that's fine, we're about to do it properly).

1. `git switch -c we-do-greeting-polish`.
2. `scripts/seed-messy-state.sh` — confirm with `git status` that you have a known dirty tree across `sample-app/`.
3. `git add -p` — stage **one** logical change, commit it. Repeat twice more, so you have three small commits. After each commit, glance at `git ls-tree -r HEAD sample-app/` and notice which blob SHA changed.
4. `git log --graph --decorate --oneline -5` — confirm your three commits sit on top of `main`.

> **Hint:** when `add -p` asks "Stage this hunk?", `y`/`n` is yes/no, `s` splits the hunk, `e` lets you hand-edit, `q` quits.

## You do (50 min)

Solo. Open a scratch terminal and a scratch notebook (`NOTES.local.md` is gitignored).
Two phases, same clone. **Do Phase 1 first** — Phase 2 resets history and would erase
Phase 1's checkpoint commit if done out of order.

### Phase 1 — spelunk the object graph, then make a focused commit

The We-do left you on a scratch branch — first return to a clean `main`:

```bash
git switch main
```

Now work through these against the existing history. Write down each answer.

1. **`app.py`'s own history.** Run `git log --oneline -- sample-app/app.py` to see every commit that touched it. Identify the one that added **`--shout`** support and the one that added **`farewell()`** — you'll reuse both below.
2. **Which commit introduced `greet()`?** Use `git log -S "def greet" --oneline -- sample-app/app.py`. Surprised where it lands? Read the full message with `git show --no-patch <SHA>`.
3. **Which commit introduced `farewell()`?** Use `git log -S "def farewell" --oneline -- sample-app/app.py`. What's the SHA, and how does it differ from the commit you found in #2?
4. **Blob SHA before `farewell()` existed.** Using the `--shout` commit from #1, read `app.py`'s blob SHA at that point with `git ls-tree <shout-SHA> sample-app/app.py`. Print it with `git cat-file -p <blob-SHA>` — confirm `farewell()` isn't there yet, and that it matches `git show <shout-SHA>:sample-app/app.py`.
5. **Tree shape at that commit.** Using *only* `git cat-file` and `git ls-tree`, list every file tracked at the `--shout` commit. How many total? Compare against `git ls-tree -r --name-only <shout-SHA>`.
6. **Make a focused commit.** Add your name to `sample-app/README.md` as a "lab participant" line. Commit it with a clear message. Then `git cat-file -p HEAD` and confirm that only the `README.md` blob entry changed (not the `app.py` blob, not the `tests/` tree).
7. **Sanity check.** Run `scripts/verify-lab.sh` — it should print a green ✅ if your focused commit is correct. Run this **now**, before Phase 2.

### Phase 2 — branch, merge, and rebase

Record your baseline now — `main` already includes your Phase 1 commit, and you'll reset
back here a few times:

```bash
git switch main
git rev-parse --short HEAD    # note this SHA — the instructions call it BASE
```

**Part A — three clean commits.**

1. `git switch -c feature/greeting-tweaks` from `main`.
2. Run `scripts/seed-messy-state.sh`. Confirm `git status` shows three changed files.
3. Use `git add -p` to produce **three separate commits**, each containing **one** of the three changes. Write a sensible message for each — imagine the reviewer needs to skim them in 30 seconds.

**Part B — compare merge styles.**

4. Branch a *second* feature branch off the same baseline: `git switch main && git switch -c feature/greeting-tweaks-noff`.
5. Cherry-pick all three commits onto it: `git cherry-pick feature/greeting-tweaks~2..feature/greeting-tweaks`.
6. Create a small unrelated commit directly on `main` (edit `sample-app/README.md`, commit it) — this prevents fast-forwards.
7. Merge the first branch with `git merge feature/greeting-tweaks` (since `main` has moved, this *cannot* fast-forward — Git creates a merge commit).
8. Reset `main` back to `BASE` plus your README commit: `git reset --hard <SHA-of-README-commit>`.
9. Now merge the *other* branch: `git merge --no-ff feature/greeting-tweaks-noff -m "Merge feature/greeting-tweaks-noff into main"`.
10. Run `git log --graph --decorate --oneline --all`. **Sketch the graph in `NOTES.local.md`.** What's the same? What's different? Where does each style help or hurt?

**Part C — linear rebase.**

11. Reset once more: `git switch main && git reset --hard BASE`. Re-apply your README commit on top.
12. `git switch feature/greeting-tweaks && git rebase main`. The three feature commits should now sit on top of the new `main` tip, with no merge commit. (Notice the feature commits got **new SHAs** — rebase rewrote them.)
13. `git switch main && git merge feature/greeting-tweaks` — this *will* fast-forward. The history is linear.
14. Compare your final `git log --graph --decorate --oneline --all` to the reference walk-through in [`instructor-notes/lab-key.md`](../instructor-notes/lab-key.md). Don't peek before you've finished Part C.

## Stretch challenges `[OPTIONAL]`

**1. Diff without `git diff`.** Pick two adjacent commits in the seeded history. Using only `git cat-file` and `git ls-tree`, determine: which files exist in commit B but not A? For files in both, which blob SHAs differ? For the changed blobs, print both and identify the changed line(s) by eye. You're reconstructing what `git diff` does internally — a tree walk plus a blob comparison. Confirm with `git diff <A> <B>`.

**2. Rebase through a conflict.** Re-do Part C, but first add a commit on `main` that edits the **same line** inside `greet()` that one of your feature commits did (the seed script's docstring change). Same-region edits on both branches are what *forces* a conflict:

```bash
git switch main
python3 - <<'PY'
from pathlib import Path
p = Path("sample-app/app.py")
t = p.read_text()
t = t.replace(
    '    message = f"Hello, {name}!"',
    '    # CONFLICT BAIT — main and your feature branch both edit greet()\n'
    '    message = f"Hello, {name}!"',
)
p.write_text(t)
PY
git commit -am "main: add a comment inside greet()"
```

Then `git switch feature/greeting-tweaks && git rebase main` — the feature commit that added a docstring to `greet()` touches the same spot, so Git halts with a conflict on that commit. Open `sample-app/app.py`, resolve (keep both the comment and the docstring), `git add sample-app/app.py`, then `git rebase --continue`. Confirm linear history with `git log --graph --decorate --oneline --all`. If you'd rather bail, `git rebase --abort` is also a valid exit.

## Debrief (15 min)

- Which of the "why VC matters" reasons resonated most with your day-to-day work?
- When does the object-model mental model *actually* matter in real life? (Hint: rebase conflicts, recovery with `git reflog`, understanding why `git mv` is just rename + commit.)
- One thing that surprised you about how Git stores files.
- Where would your team prefer **merge** over **rebase**, and why? Are there situations where the opposite is true?
- If a teammate committed straight to `main` and pushed it: what do they do *now*?
- Which commands do you want to alias? (e.g., `git lg` for `log --graph --decorate --oneline --all`)
