# Lab 01 — Git Fundamentals

Day 1 of the [CI/CD for Ignition Masterclass](https://github.com/mustry-academy/cicd-masterclass).

> Build a working mental model of Git, and learn to operate confidently with branches, commits, merges, and rebases.

This is the first lab in the course. We deliberately stay out of Ignition territory for now — the only subject of our Git exercises is a tiny generic Python app in [`sample-app/`](./sample-app/). Ignition-specific deployments arrive in Lab 03.

## Prerequisites

- Pass [`cicd-preflight`](https://github.com/mustry-academy/cicd-preflight)
- Clone this repo before the live session

## Quick start

```bash
gh repo clone mustry-academy/cicd-lab-01-git-fundamentals
cd cicd-lab-01-git-fundamentals
python -m venv .venv && source .venv/bin/activate
pip install -r sample-app/requirements.txt
pytest sample-app/tests
```

## Lab structure

One continuous ~3-hour lab that interleaves Git's object model with everyday workflows, so the model becomes the lens for every command you run. The full walk-through lives in [`exercises/lab.md`](./exercises/lab.md):

- Why version control matters
- The object model (commit/tree/blob) — hands-on the workflow
- Everyday workflows: `add -p`, `switch`, branch, merge (fast-forward vs `--no-ff`), rebase, and recovery
- A solo spelunk-then-build exercise, plus optional stretch challenges

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
