## Coding Style

To keep the codebase clean and readable, PEP8 standards are enforced using [Ruff](https://docs.astral.sh/ruff/). To make this frictionless, a Github Action automatically format and lint code on the server.

## How the Automation Works

1. Code is pushed to a branch on github
2. A GitHub Action intercepts the push
3. The action runs Ruff to fix unused imports, correct spacing and character line limit
4. A new commit is automatically created and pushed back to the branch

Because the action pushes commits to your branch, the remote branch will be one commit ahead. You will need to pull the autofixed code before you can push again.

## Recommended IDE Setup

GitHub Codespaces and VS Code can be configured to automatically handle these syncs in the background so you never experience a merge conflict with the bot.

Add the following to your Workspace `settings.json`:

```json
{
    "git.autofetch": "all",
    "git.enableSmartCommit": true,
    "git.postCommitCommand": "sync"
}
```

With these settings, VS Code will automatically pull the bot's changes before pushing your new commit.

## Modifying Rules

The linting rules are located in `pyproject.toml`. We ignore `E501` (line to long) in the linter to let the Ruff formatter handle line wrapping. 