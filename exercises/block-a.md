# Block A — Why version control (VC) matters; Git's object model demystified

**Duration:** ~90 minutes
* 20 min why version control
* 15 min object-model demo
* 15 min we-do
* 30 min you-do
* 10 min debrief

## Goal

You should leave this block able to:

- Articulate **three concrete reasons** version control matters in software work
- Describe what a **commit**, **tree**, and **blob** physically are inside `.git/objects/`
- Use `git cat-file`, `git ls-tree`, and `git log -S` to explore a repository's object graph
- Explain in your own words what HEAD, refs, and the index do

## Pre-flight

```bash
git fetch --tags
git checkout block-a-start
```

You should now see a `sample-app/` directory with several commits already in its history. Run `git log --oneline` and confirm you see at least five commits.

If you'd like to read ahead: [`docs/why-version-control.md`](../docs/why-version-control.md) and [`docs/git-object-model.md`](../docs/git-object-model.md).

## I do — Why version control matters (20 min)

The instructor walks through:

1. **Pre-VC pain.** `FINAL_v2_actual_REAL.zip`, lost work, no audit trail. Anyone who's been in industry long enough has a story.
2. **What a Version Control System (VCS) gives you.** History, blame, branching, safe undo. Show a single `git blame` on `sample-app/app.py` to make the point.
3. **Centralized vs distributed.** Why Git won. Why "every clone is a full backup" matters when the central server is down.
4. **Live folder-vs-repo contrast.** `mkdir scratch && cd scratch && echo hi > a.txt`. Then the same with `git init`. What's tracked? What isn't? What happens when you change `a.txt`?

This segment ends with a one-sentence prompt the group answers around the room: *"What's a version-control disaster you've personally lived through, or watched somebody else live through?"*

## I do — Git's object model (15 min)

The instructor walks the `sample-app/` history live:

1. `git log --oneline` — note one commit's SHA, e.g. `a1b2c3d`.
2. `git cat-file -p a1b2c3d` — read the commit object out loud. Note the `tree` line.
3. `git cat-file -p <tree-SHA>` — read the tree object. It lists blobs and sub-trees by SHA.
4. `git cat-file -p <blob-SHA>` — see the raw file content.
5. Sketch the commit → tree → blob graph on the board.
6. Show `git log --graph --decorate --oneline --all` — the same graph, in commit form.

Key points: commits point to a *single* tree; trees point to blobs; blobs are *just* content (no filename). The filename lives in the tree entry.

## We do (15 min)

Following along on your own clone:

1. Make a small change to `sample-app/README.md` — add a single sentence.
2. `git add sample-app/README.md && git commit -m "docs: expand sample-app intro"`
3. `git log --oneline` — note your new commit's SHA.
4. `git cat-file -p <your-commit-SHA>` — read it out loud. Note the `tree` SHA and the `parent` SHA.
5. `git cat-file -p <tree-SHA>` — find the entry for `README.md`. Note its blob SHA.
6. `git cat-file -p <blob-SHA>` — confirm it matches your new file content.
7. `git ls-tree HEAD sample-app/` — see the tree expressed in one line.
8. `git log --graph --decorate --oneline --all` — observe your commit at the tip.

## You do (30 min)

Solo spelunking on the existing history at `block-a-start`. Open a scratch notebook — write down each answer.

1. **Blob SHA at `HEAD~2`.** Find the blob SHA that `sample-app/app.py` had at `HEAD~2`. Use `git ls-tree HEAD~2 sample-app/app.py`. Print the blob with `git cat-file -p <blob-SHA>` — does it match what `git show HEAD~2:sample-app/app.py` shows?
2. **Which commit introduced `greet()`?** Use `git log -S "def greet" --oneline -- sample-app/app.py`. What's the SHA? Read the full commit message with `git show --no-patch <SHA>`.
3. **Tree shape at `HEAD~1`.** Using *only* `git cat-file` and `git ls-tree`, list every file tracked at `HEAD~1`. How many files total? Compare against `git ls-tree -r --name-only HEAD~1`.
4. **Make a focused commit.** Add your name to `sample-app/README.md` as a "lab participant" line. Commit it with a clear message. Then `git cat-file -p HEAD` and confirm that only the `README.md` blob entry changed (not the `app.py` blob, not the `tests/` tree).
5. **Sanity check.** Run `scripts/verify-block-a.sh` — it should print a green ✅ if your block-a-end state is correct.

Capture your answers in `NOTES.local.md` (gitignored). Don't worry about wording — just the SHAs and the commit messages.

## Stretch challenge `[OPTIONAL]`

**Diff without `git diff`.** Pick two adjacent commits in the seeded history. Using only `git cat-file` and `git ls-tree`, determine:

- Which files exist in commit B but not commit A?
- For files in both, which blob SHAs are different?
- For the changed blobs, print both and identify the changed line(s) by eye.

You're reconstructing what `git diff` does internally. When you're done, run `git diff <A> <B>` and confirm your manual answer matches.

## Debrief (10 min)

- Which of the "why VC matters" reasons resonated most with your day-to-day work?
- When does the object-model mental model *actually* matter in real life? (Hint: rebase conflicts, recovery with `git reflog`, understanding why `git mv` is just rename + commit.)
- One thing that surprised you about how Git stores files.
