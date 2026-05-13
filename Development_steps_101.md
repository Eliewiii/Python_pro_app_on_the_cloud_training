
## 🛠️ Development Setup

Follow these steps to set up the repository locally on a Linux environment.

### 1. Setup repository in GitHub abd Clone the Repository
Open your terminal and run:
```bash
# Clone the repo from GitHub
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)

# Enter the project directory
cd YOUR_REPO_NAME

#Open this specific folder in VS Code
code .
```

Make the main branch with pull request only

### 2. make venv

```bash
python -m venv .venv

source .venv/bin/activate

pip install fastapi uvicorn pytest numpy
```




#### Git actions CL

# Git & GitHub Professional Workflow

### 1. Setup & Status
Commands to check the current state of your repository.

| Command | Description |
| :--- | :--- |
| `git status` | Shows the current state of your working directory and staging area. |
| `git diff` | Shows the exact line changes in your files before you stage them. |
| `git log --oneline --graph` | Displays a clean, visual history of your commits. |

---

### 2. Staging & Committing
The process of preparing your code for a "snapshot."

| Command | Description |
| :--- | :--- |
| `git add core/` | Stages an entire directory (like your engine logic). |
| `git add .` | Stages all changes in the current directory (respects `.gitignore`). |
| `git commit -m "feat: <message>"` | Records your changes. Use `feat:`, `fix:`, or `refactor:` prefixes. |
| `git commit --amend` | Allows you to edit the last commit message if you made a typo. |
| `git rm -r --cached .vscode/` | Remove files from folder recursively from tracking |

---

### 3. Branching (Feature Workflow)
Essential for R&D. Never work directly on `main` when experimenting with new algorithms.

| Command | Description |
| :--- | :--- |
| `git checkout -b feature/name` | Creates a new branch and switches to it immediately. |
| `git branch` | Lists all local branches. |
| `git checkout main` | Switches back to your stable production branch. |
| `git merge <branch_name>` | Merges the completed feature back into your main code. |
| `git branch -d branch_name` | Delete a branch |

---

### 4. Cloud Synchronization (GitHub)
Moving your local work to the cloud for backup and collaboration.

| Command | Description |
| :--- | :--- |
| `git remote -v` | Verifies which GitHub repository your local folder is connected to. |
| `git push origin main` | Uploads your local commits to the GitHub cloud. |
| `git pull origin main` | Downloads the latest version from GitHub. |
| `git clone <url>` | Downloads a full project from GitHub to a new machine. |
| `git fetch --all` | update all |

---

### 5. Maintenance & Safety
Keeping the repository clean and recovering from mistakes.

| Command | Description |
| :--- | :--- |
| `git rm -r --cached .` | Clears the git cache (useful if you updated `.gitignore`). |
| `git checkout -- <file>` | Discards local changes to a file and restores it. |
| `git stash` | Temporarily "hides" uncommitted changes to switch branches quickly. |



### Ruff

To Check: `ruff check .` — This lists all linting violations in your project.  

To Fix: `ruff check --fix .` — This automatically fixes "safe" errors, like unused imports or incorrectly ordered ones.  

To Format: `ruff format .` — This reformats your spacing and line lengths to match your 100-character rule.