# Connect External Repositories

Use skills from other GitHub repositories without copying files.

## Quick Start

```
Connect https://github.com/obra/superpowers
```

This clones the repo and makes its skills available to Claude.

## Commands

| Command | What It Does |
|---------|--------------|
| `Connect {url}` | Clone a repo and register its skills |
| `List connected repos` | Show all connected repositories |
| `Update connected repos` | Pull latest changes from all repos |
| `Disconnect {name}` | Remove a connected repository |
| `Use {skill} from {repo}` | Use a specific skill from a connected repo |

## Examples

### Connect a Popular Skills Repo

```
Connect obra/superpowers
```

### Use a Skill from Connected Repo

```
Use the brainstorming skill from superpowers
```

### See What's Connected

```
What repos are connected?
```

### Get Latest Updates

```
Update all connected repos
```

## How It Works

1. **Clones** the repo to `~/.claude/connected-repos/{name}/`
2. **Discovers** skills (looks for `SKILL.md` or `CLAUDE.md` files)
3. **Registers** in `~/.claude/connected-repos.json`
4. **Skills become available** to use alongside PM Agent skills

## Benefits

✅ **Always up-to-date** - `git pull` to get latest  
✅ **No file duplication** - Skills stay in their source repo  
✅ **Clear attribution** - Know where each skill came from  
✅ **Easy contribution** - Submit fixes back to source  

## Popular Skill Repositories

| Repository | Description |
|------------|-------------|
| [obra/superpowers](https://github.com/obra/superpowers) | General-purpose Claude skills (brainstorming, debugging, etc.) |

*Know a good skills repo? Add it here!*

## Troubleshooting

### "Repository not found"
- Check the URL is correct
- For private repos, ensure you have access
- Try cloning manually: `git clone {url}`

### Skills not appearing
- The repo might not have a `skills/` folder
- Skills need `SKILL.md` or `CLAUDE.md` files to be discovered

### Update failed
- Check network connection
- Run `cd ~/.claude/connected-repos/{name} && git status` to see issues

## File Locations

| Path | Purpose |
|------|---------|
| `~/.claude/connected-repos/` | Where cloned repos live |
| `~/.claude/connected-repos.json` | Registry of connected repos |