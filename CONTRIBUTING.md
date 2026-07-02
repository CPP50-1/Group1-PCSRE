## Coding Style

To keep our codebase clean, readable, and universally consistent, we strictly enforce PEP 8 standards using [Ruff](https://docs.astral.sh/ruff/). 

### Prerequisites

Before setting up the hooks, ensure you have the following installed on your system:

* **Git** (to clone the repository and commit changes)
* **Python** (to run the environment)

### Setting Up Pre-Commit Hooks

We use the `pre-commit` framework to automatically run Ruff on your code before it gets committed. 

1. **Install the dependencies:**
   `pre-commit` is included in our project requirements. Install it by running:
    ```bash
    pip install -r requirements.txt
    ```

2. **Install the git hook scripts:**
    Link the hooks to your local git repository:
    ```bash
    pre-commit install
    ```

Once installed, Ruff will automatically lint and format your modified files every time you run `git commit`. If Ruff finds issues it cannot automatically fix, the commit will be blocked until you resolve them.