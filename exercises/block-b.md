# Block B — Everyday workflows: add, commit, branch, merge, rebase

**Duration:** ~90 minutes (20 min demo, 15 min we-do, 35 min you-do, 10 min debrief, ~10 min buffer)

## Goal

You should leave this block able to:

- Stage hunks selectively with `git add -p`
- Use `git switch` and `git switch -c` confidently
- Choose between **merge** (fast-forward vs `--no-ff`) and **rebase** deliberately, and explain the tradeoffs
- Clean up history with `git rebase -i` before review
- Recover from "oh no I committed to the wrong branch"

## Pre-flight

```bash
git fetch --tags
git checkout block-b-start
chmod +x scripts/seed-messy-state.sh
```

Confirm `main` is clean (`git status` should be empty) and the seed script is available.

## I do (20 min)

Live-coded demo. Follow along with your eyes, not your keyboard:

1. **Make a mess.** The instructor runs `scripts/seed-messy-state.sh` to drop three unrelated edits across `sample-app/`.
2. **Stage by hunk.** `git add -p` to stage them as three logical commits.
3. **Branch deliberately.** `git switch -c feature/greeting-polish`.
4. **Merge — fast-forward.** Show that when `main` hasn't moved, `git merge feature/greeting-polish` *fast-forwards*. There's no merge commit. The history is linear.
5. **Merge — `--no-ff`.** Reset, advance `main` with a separate commit, then `git merge --no-ff feature/greeting-polish`. There **is** a merge commit. The history shows the branch shape. Display both with `git log --graph --decorate --oneline --all`.
6. **Interactive rebase.** `git rebase -i HEAD~3` — reorder, squash, reword. Show the commit SHAs change because rebase rewrites history.
7. **Oops-recovery.** "Oops, committed to main." Demo `git reset HEAD~1 --soft` to keep the changes in the index, then `git switch -c feature/recovered` and `git commit`.

## We do (15 min)

Follow along on your own clone:

1. `git switch -c we-do-greeting-polish` from `block-b-start`.
2. `scripts/seed-messy-state.sh` — confirm with `git status` that you have a known dirty tree.
3. `git add -p` — stage **one** logical change, commit it. Repeat twice more, so you have three small commits.
4. `git log --graph --decorate --oneline -5` — confirm your three commits sit on top of `block-b-start`.

You don't need to do the merge/rebase steps here — you'll do those in the solo exercise.

## You do (35 min)

Solo. Open a scratch terminal alongside the instructions.

### Part 1 — Three clean commits

1. Reset to a clean baseline: `git checkout block-b-start && git switch -c feature/greeting-tweaks`.
2. Run `scripts/seed-messy-state.sh`. Confirm `git status` shows three changed files.
3. Use `git add -p` to produce **three separate commits**, each containing **one** of the three changes. Write a sensible message for each — imagine the reviewer needs to skim them in 30 seconds.

> **Hint:** when `add -p` asks "Stage this hunk?", `y`/`n` is yes/no, `s` splits the hunk, `e` lets you hand-edit. `q` quits.

### Part 2 — Compare merge styles

4. Switch back to `main`. Branch a *second* feature branch off the same baseline: `git switch main && git switch -c feature/greeting-tweaks-noff`.
5. Cherry-pick all three commits from `feature/greeting-tweaks` onto this new branch: `git cherry-pick feature/greeting-tweaks~2..feature/greeting-tweaks`.
6. Now create a small unrelated commit directly on `main` (edit `sample-app/README.md`, commit it) — this prevents fast-forwards.
7. Merge `feature/greeting-tweaks` into `main` with `git merge feature/greeting-tweaks` (note: since `main` has moved, this *cannot* fast-forward — Git creates a merge commit).
8. Reset `main` back to `block-b-start` plus your README commit: `git reset --hard <SHA-of-README-commit>`.
9. Now merge the *other* branch: `git merge --no-ff feature/greeting-tweaks-noff -m "Merge feature/greeting-tweaks-noff into main"`.
10. Run `git log --graph --decorate --oneline --all`. **Sketch the graph in `NOTES.local.md`.** What's the same? What's different? Where does each style help or hurt?

### Part 3 — Linear rebase

11. Reset once more: `git checkout main && git reset --hard block-b-start`. Re-apply your README commit on top.
12. `git switch feature/greeting-tweaks && git rebase main`. The three feature commits should now sit on top of the new `main` tip, with no merge commit.
13. `git switch main && git merge feature/greeting-tweaks` — this *will* fast-forward. The history is linear.
14. Final state of `git log --graph --decorate --oneline --all` should match `block-b-end`.

### Sanity check

Compare your `git log --graph --decorate --oneline --all` to the reference walk-through in [`instructor-notes/block-b-key.md`](../instructor-notes/block-b-key.md). Don't peek before you've finished Part 3.

## Stretch challenge `[OPTIONAL]`

**Rebase through a conflict.** Re-do Part 3, but first run:

```bash
git switch main
echo "# CONFLICT BAIT" >> sample-app/app.py
git commit -am "main: add header comment to app.py"
```

Then `git switch feature/greeting-tweaks && git rebase main` — one of your feature commits also touched `app.py`. Git will halt with a conflict on a specific commit. Open `sample-app/app.py`, resolve, `git add`, then `git rebase --continue`. When done, run `git log --graph --decorate --oneline --all` and confirm linear history.

If you want, undo the whole rebase with `git rebase --abort` instead — also a valid exit.

## Debrief (10 min)

- What was the hardest moment?
- Which commands do you want to alias? (e.g., `git lg` for `log --graph --decorate --oneline --all`)
- Where would your team prefer **merge** over **rebase**, and why? Are there situations where the opposite is true?
- If a teammate committed straight to `main` and pushed it: what do they do *now*?
