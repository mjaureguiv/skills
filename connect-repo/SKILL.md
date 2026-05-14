---
name: connect-repo
description: "Connect external GitHub repositories to access their skills. Use when user wants to use skills from other repos like obra/superpowers, link external skill libraries, or manage connected repositories."
version: 1.0.0
user-invokable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

# Connect External Repositories

This skill manages connections to external GitHub repositories, allowing you to use skills from other sources like [obra/superpowers](https://github.com/obra/superpowers).

## Commands

### Connect a New Repository

**User says:** "Connect https://github.com/obra/superpowers" or "Add the superpowers repo"

**Action:**
1. Parse the GitHub URL to extract owner/repo
2. Clone to `~/.claude/connected-repos/{repo-name}/`
3. Register in `~/.claude/connected-repos.json`
4. Add the repo to VS Code workspace (optional)
5. Display available skills from the connected repo

```bash
# Clone the repository
REPO_URL="$1"
REPO_NAME=$(basename "$REPO_URL" .git)
REPOS_DIR="$HOME/.claude/connected-repos"

mkdir -p "$REPOS_DIR"
git clone "$REPO_URL" "$REPOS_DIR/$REPO_NAME"
```

### List Connected Repositories

**User says:** "List connected repos" or "What repos are connected?"

**Action:**
1. Read `~/.claude/connected-repos.json`
2. For each repo, check if it exists and show status
3. List available skills from each repo

```bash
# List all connected repos
cat ~/.claude/connected-repos.json | jq -r '.repos[] | "\(.name): \(.url)"'

# Or list directories
ls -la ~/.claude/connected-repos/
```

### Update Connected Repositories

**User says:** "Update connected repos" or "Pull latest from connected repos"

**Action:**
1. Read `~/.claude/connected-repos.json`
2. For each repo, run `git pull`
3. Report any updates

```bash
# Update all connected repos
for dir in ~/.claude/connected-repos/*/; do
  echo "Updating $(basename "$dir")..."
  (cd "$dir" && git pull)
done
```

### Disconnect a Repository

**User says:** "Disconnect superpowers" or "Remove the superpowers repo"

**Action:**
1. Confirm with user before deleting
2. Remove from `~/.claude/connected-repos.json`
3. Optionally delete the cloned directory
4. Remove from VS Code workspace if added

```bash
# Remove a connected repo
REPO_NAME="$1"
rm -rf ~/.claude/connected-repos/"$REPO_NAME"
```

### Use a Skill from Connected Repo

**User says:** "Use brainstorming skill from superpowers"

**Action:**
1. Find the skill in connected repos
2. Read its SKILL.md or CLAUDE.md
3. Execute the skill with context from both repos

---

## Configuration File Format

Location: `~/.claude/connected-repos.json`

```json
{
  "repos": [
    {
      "name": "superpowers",
      "url": "https://github.com/obra/superpowers.git",
      "localPath": "~/.claude/connected-repos/superpowers",
      "connectedAt": "2026-03-11T15:45:00Z",
      "lastUpdated": "2026-03-11T15:45:00Z",
      "skills": [
        "brainstorming",
        "code-review",
        "debugging"
      ]
    }
  ]
}
```

---

## Workflow: Connect a New Repository

When user asks to connect a repository, follow these steps:

### Step 1: Parse the URL

Extract repository information from various URL formats:
- `https://github.com/owner/repo`
- `https://github.com/owner/repo.git`
- `git@github.com:owner/repo.git`
- `owner/repo` (assume github.com)

### Step 2: Check Prerequisites

```bash
# Ensure directory exists
mkdir -p ~/.claude/connected-repos

# Ensure config file exists
if [ ! -f ~/.claude/connected-repos.json ]; then
  echo '{"repos":[]}' > ~/.claude/connected-repos.json
fi
```

### Step 3: Clone the Repository

```bash
REPO_URL="https://github.com/obra/superpowers.git"
REPO_NAME="superpowers"

git clone "$REPO_URL" ~/.claude/connected-repos/"$REPO_NAME"
```

### Step 4: Discover Skills

Look for skills in common locations:
- `skills/` directory
- `.claude/skills/` directory
- Any folder with `SKILL.md` or `CLAUDE.md`

```bash
# Find all skills in the repo
find ~/.claude/connected-repos/superpowers -name "SKILL.md" -o -name "CLAUDE.md" | head -20
```

### Step 5: Update Config

Use the write tool to update `~/.claude/connected-repos.json` with:
- Repository name, URL, local path
- List of discovered skills
- Timestamp

### Step 6: Optional VS Code Integration

Ask user if they want to add the repo to their VS Code workspace:

> "Would you like me to add this repo to your VS Code workspace so you can browse its files?"

If yes, guide them to: File → Add Folder to Workspace → select the cloned directory

### Step 7: Show Available Skills

Display a summary:

```
✓ Connected: superpowers
  Location: ~/.claude/connected-repos/superpowers
  
  Available skills:
  • brainstorming - Creative ideation and problem-solving
  • code-review - Structured code review process
  • debugging - Systematic debugging approach
  
  To use a skill: "Use the brainstorming skill from superpowers"
```

---

## Using Skills from Connected Repos

When user wants to use a skill from a connected repo:

1. **Find the skill file:**
   ```bash
   cat ~/.claude/connected-repos/superpowers/skills/brainstorming/SKILL.md
   ```

2. **Read and apply** the skill's instructions

3. **Use context from both repos:**
   - The PM Agent's context (product info, templates)
   - The skill's instructions and patterns

---

## Error Handling

### Repository Already Connected
```
⚠ Repository 'superpowers' is already connected.
  Location: ~/.claude/connected-repos/superpowers
  
  Would you like to:
  1. Update it (git pull)
  2. Reconnect (delete and re-clone)
  3. Cancel
```

### Clone Failed
```
✗ Failed to clone repository
  
  Possible issues:
  • Repository doesn't exist or is private
  • No network connection
  • Git not installed
  
  Try:
  • Check the URL is correct
  • Ensure you have access (for private repos)
  • Run: git clone {url} manually to see detailed error
```

### Skills Directory Not Found
```
⚠ No skills directory found in this repository.
  
  Looked in:
  • skills/
  • .claude/skills/
  
  This repo might not follow the standard skills format.
  You can still browse it manually at: ~/.claude/connected-repos/{name}
```

---

## Popular Repositories to Connect

| Repository | Description | Connect Command |
|------------|-------------|-----------------|
| [obra/superpowers](https://github.com/obra/superpowers) | General-purpose Claude skills | `Connect obra/superpowers` |

*Add more popular skill repos here as the community grows*

---

## Tips

### Keep Repos Updated
Run "Update connected repos" periodically to get the latest skills.

### Organize by Purpose
Connect repos that complement your work:
- PM-focused repos for product work
- Dev-focused repos for technical tasks
- Company-specific repos for internal tools

### Contribute Back
Found a bug or improvement? The skill is in `~/.claude/connected-repos/{name}`, and you can submit PRs to the source.