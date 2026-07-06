# Lab 01 — Git Fundamentals

Day 1 of the [CI/CD for Ignition Masterclass](https://github.com/mustry-academy/cicd-masterclass).

> Build a working mental model of Git, and learn to operate confidently with branches, commits, merges, and rebases.

This is the first lab in the course. We deliberately stay out of Ignition territory for now — the only subject of our Git exercises is a tiny generic Python app in [`sample-app/`](./sample-app/). Ignition-specific deployments arrive later in the series.

## Prerequisites

- Pass [`cicd-preflight`](https://github.com/mustry-academy/cicd-preflight)
- **Fork this repo** to your own GitHub account and clone *your fork* before the live session — every lab repo gets forked to your personal space, so you can commit, branch and push freely

## Quick start

```bash
gh repo fork mustry-academy/cicd-lab-01-git-fundamentals --clone   # fork to your account + clone your fork
cd cicd-lab-01-git-fundamentals
python -m venv .venv && source .venv/bin/activate
pip install -r sample-app/requirements.txt
pytest sample-app/tests
```

## Lab structure

One continuous ~3-hour lab (09:00–12:00) that interleaves Git's object model with everyday workflows, so the model becomes the lens for every command you run. The full walk-through lives in [`exercises/lab.md`](./exercises/lab.md):

- **Introduction** — welcome to the series and how the labs work
- **The Oatmakers story** — a fictional client (eight Ignition sites, zero CI/CD) sets the stage for why this series exists
- **Teaching** — what Git is, the object model (blob/tree/commit/branch/HEAD), the merge · rebase · cherry-pick workflows, remotes & tags, the command vocabulary, `git blame`/`git reset`, and `.gitignore`
- **We-do** — the instructor live-codes the moves: `add`/`commit`, `switch`, branch, merge (fast-forward vs `--no-ff`), rebase, and recovery
- **You-do (breakout rooms)** — a guided warm-up, then a solo spelunk-then-build exercise, plus optional stretch challenges
- **Wrap-up & questions**

## Repo layout

```
cicd-lab-01-git-fundamentals/
├── README.md
├── exercises/
│   └── lab.md
├── docs/                         ← reference reading
│   ├── why-version-control.md
│   └── git-object-model.md
├── instructor-notes/             ← answer key (read after solo work)
│   └── lab-key.md
├── slides/                       ← the presented decks, in session order
│   ├── introduction.html
│   ├── oatmakers-story.html
│   ├── teaching.html
│   ├── assignment.html
│   └── logos/
├── scripts/
│   ├── seed-messy-state.sh       ← deterministic dirty working tree for the workflow phase
│   └── verify-lab.sh             ← sanity-check the solo focused-commit step
└── sample-app/                   ← the tiny Python app we'll version together
    ├── app.py
    ├── requirements.txt
    ├── tests/
    │   └── test_app.py
    └── README.md
```

## Licence

Apache 2.0 — see [`LICENSE`](./LICENSE).
