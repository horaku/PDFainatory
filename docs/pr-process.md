# PR Process Notes (Codex / branch update limitation)

## Problem
If you see:

`Codex does not currently support updating PRs that are updated outside of Codex. For now, please create a new PR.`

it means the existing PR branch diverged due to updates performed outside the active Codex flow (e.g. direct GitHub edits, manual push/rebase, or merge actions).

## Required Operator Action
1. Create a new branch from the latest target base branch.
2. Move the required commits into that branch (or continue from current `HEAD` if already correct).
3. Open a **new PR**.
4. Link the old PR and close it after reviewers switch context.

## Clean Replacement PR Flow (repository default)
Use this sequence when asked to create a fresh PR from the current workspace state.

```bash
# from repository root
# 1) verify workspace branch/state
git status --short
git branch --show-current

# 2) create a fresh branch with codex-fixed naming
BRANCH_NAME="codex-fixed-translation-job"
git checkout -b "$BRANCH_NAME"

# 3) if there are unresolved merge conflicts, prefer workspace versions
#    (keeps current tree content as source of truth)
git checkout --ours .
git add -A

# 4) commit all current workspace files as-is
git commit -m "Create clean replacement PR branch from current workspace state"

# 5) push and open a brand-new PR (do not update old PR)
git push -u origin "$BRANCH_NAME"
```

## Notes on conflict preference
- During conflict resolution for this recovery flow, prefer the **current workspace content** (equivalent to `--ours` on the active branch).
- Re-run validations after conflict resolution before creating the new PR.

## Development Rule for this Repository
- If PR update is blocked by Codex/GitHub integration constraints, do **not** spend cycles trying to update the old PR branch.
- Create a replacement PR immediately and continue delivery there.
