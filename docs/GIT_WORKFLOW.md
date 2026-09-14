# Zoriel Git Workflow

`main` must remain runnable.

Use feature branches for meaningful changes:

```bash
git checkout -b feature/intent-engine
git add .
git commit -m "feat: add structured intent engine"
git checkout main
git merge --no-ff feature/intent-engine
git tag v0.3.0
```

ZIP files are release artifacts only. The Git repository is the canonical source of truth.
