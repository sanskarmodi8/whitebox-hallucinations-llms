# Contributing

Follow these rules for a smooth collaboration.

## Branches & commits
- Branch name: `feat/<name>-<task>`, `fix/<name>-<bug>`, `docs/<what>`.
- Use Conventional Commits in commit messages (e.g. `feat: add decoding config`).

## PR requirements
- Link the issue number (if any).
- Add a short description and smoke test results.
- Add the run manifest/config if the PR changes experiment behavior.

## Run artifacts
- For each run, commit only `experiments/<run>/config_used.yaml` and `run-manifest.json` and a *small* `predictions.jsonl`. Big result files should be stored externally and linked.

## Review
- At least one team review required before merging.
- CI must pass.
