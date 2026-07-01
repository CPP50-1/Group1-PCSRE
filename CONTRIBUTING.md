## Coding Style

To keep our codebase clean, readable, and universally consistent, we strictly enforce PEP8 standards using [Ruff](https://docs.astral.sh/ruff/).

To make this workflow as frictionless as possible, you do not need to install any local formatting tools. Instead, a GitHub Action automatically formats and lints your code directly on the server.

### How the Automation Works

1. You push code to a branch on GitHub.
2. A GitHub Action intercepts the push.
3. The action runs Ruff to enforce character line limits, correct spacing, and fix minor issues like unused imports.
4. A new commit containing the fixed code is automatically created and pushed back to your branch.

### ⚠️ The "Git Pull" Rule & Divergent Branches

Because the GitHub Action pushes commits directly to your remote branch, the server will frequently be one commit ahead of your local machine. If you continue typing locally and attempt to push again, your push will be rejected.

If you run `git pull` and receive a **"divergent branches"** fatal error, it means your new local commits conflict with the bot's formatting commit.

**The Fix:** You must rebase your local changes on top of the bot's formatting. Run this command once to set your global Git preference:

```bash
git config --global pull.rebase true

```

Once this is set, running `git pull` will seamlessly apply the bot's formatting first and cleanly replay your local commits on top of it.

### Recommended IDE Setup (Avoid Conflicts Entirely)

If you use GitHub Codespaces or VS Code, you can configure your editor to handle these syncs automatically in the background, ensuring you never experience a merge conflict with the bot.

Add the following to your Workspace or User `settings.json`:

```json
{
    "git.autofetch": "all",
    "git.enableSmartCommit": true,
    "git.postCommitCommand": "sync"
}

```

**Why this works:** With these settings enabled, VS Code continuously fetches the bot's changes in the background. The exact moment you click "Commit," VS Code automatically pulls the formatted code *before* creating your local commit. This ensures your new work is safely stacked on top of the clean codebase, bypassing the need for a manual rebase entirely.

*(Note: If the team prefers not to use these IDE settings and manual rebasing becomes a bottleneck, we will upgrade to local pre-commit hooks to format code before it is pushed).*

### Modifying Rules

All linting and formatting configurations are located in `pyproject.toml`.

We explicitly ignore rule `E501` (Line too long) in the linter. This prevents the workflow from failing on intentionally long strings or URLs, allowing the Ruff formatter to handle standard line wrapping safely.