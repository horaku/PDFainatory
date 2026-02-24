# PR Process Notes (Codex / branch update limitation)

## Problem
If you see:

`Codex does not currently support updating PRs that are updated outside of Codex. For now, please create a new PR.`

it means the existing PR branch diverged due to updates performed outside the active Codex flow (e.g. direct GitHub edits, manual push/rebase, or merge actions).

## Required Operator Action
1. Create a new branch from the latest target base branch.
2. Move the required commits into that branch (or continue from current HEAD if already correct).
3. Open a **new PR**.
4. Link the old PR and close it after reviewers switch context.

## Recommended Command Sequence
```bash
# from repository root
# 1) ensure you are on the branch containing final changes
git checkout work

# 2) create a fresh branch for the replacement PR
git checkout -b fix/new-pr-replacement

# 3) verify history and state
git log --oneline -n 10
git status --short

# 4) push (if remote is configured)
git push -u origin fix/new-pr-replacement
```

## Development Rule for this Repository
- If PR update is blocked by Codex/GitHub integration constraints, do **not** spend cycles trying to update the old PR branch.
- Create a replacement PR immediately and continue delivery there.
