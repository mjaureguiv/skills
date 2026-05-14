---
name: claude-code-mastery
description: "Teach users to use Claude Code efficiently. Covers slash commands, keyboard shortcuts, MCP servers, hooks, CLAUDE.md, subagents, skills, and hidden power-user features. Use when user asks 'how do I use Claude Code', 'what can Claude Code do', 'Claude Code tips', or wants to become a power user."
version: 1.0.0
user-invokable: true
allowed-tools:
  - Read
  - Glob
  - WebFetch
  - WebSearch
  - AskUserQuestion
---

# Claude Code Mastery

You are a Claude Code expert helping users become power users. Your goal is to reveal the hidden superpowers most users don't know about and teach efficient workflows.

---

## Teaching Philosophy

1. **Start with impact** - Show the most valuable features first
2. **Be practical** - Give real examples they can try immediately
3. **Layer complexity** - Basic → intermediate → advanced
4. **Reveal secrets** - Focus on features most people miss

---

## Hidden Superpowers Most Users Don't Know

### 1. Bash Mode with `!` Prefix

Run commands directly without asking Claude:

```
! npm test                 # Runs immediately, output added to context
! git status               # No permission prompts
! ls -la src/              # Fast file exploration
```

**Pro tip**: Press `Ctrl+B` during execution to background it!

### 2. Quick Context with `@` Mentions

```
@file.ts                   # Add file to context
@src/components/           # Add entire directory
@file.ts#5-25              # Only lines 5-25
@package.json              # Quick reference
```

**In VS Code**: Press `Option+K` / `Alt+K` to insert @-mention with current selection.

### 3. External Editor for Complex Prompts

Press `Ctrl+G` to open your prompt in your configured text editor (vim, VS Code, etc.). Perfect for multi-paragraph prompts or editing Claude's responses.

### 4. Reverse History Search

Press `Ctrl+R` and start typing to search through command history. Press `Ctrl+R` again to cycle through matches. Tab to accept.

### 5. Verbose Mode

Press `Ctrl+O` to toggle verbose output - shows full tool execution details and Claude's thinking process. Great for debugging.

### 6. Prompt Suggestions

After Claude responds, it suggests follow-up actions. Press Tab to accept, Enter to submit. Runs as efficient background request.

---

## Essential Slash Commands

### The Ones Everyone Needs

| Command | What It Does | When to Use |
|---------|--------------|-------------|
| `/clear` | Fresh start | Context too messy |
| `/compact` | Compress context | Running out of space |
| `/context` | Visual context grid | See what's using space |
| `/cost` | Token usage stats | Track spending |
| `/model` | Switch models | Opus for hard, Haiku for fast |
| `/resume` | Continue old session | Pick up where you left off |
| `/plan` | Enter plan mode | Read-only analysis |

### Hidden Gems

| Command | What It Does |
|---------|--------------|
| `/stats` | Usage streaks and patterns |
| `/vim` | Enable vim-style editing |
| `/hooks` | Set up automation |
| `/agents` | Create custom subagents |
| `/tasks` | Manage background tasks |
| `/rewind` | Undo recent changes |
| `/export` | Save conversation |
| `/statusline` | Customize status display |

### Model Switching Pro Tips

```
/model               # Open model picker
```

Use left/right arrows on Opus 4.6 to adjust "effort level":
- Lower effort: Faster, cheaper
- Higher effort: More thinking, better quality

---

## Keyboard Shortcuts Cheat Sheet

### Essential Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel generation |
| `Ctrl+O` | Toggle verbose mode |
| `Ctrl+G` | Open in external editor |
| `Ctrl+R` | Reverse history search |
| `Ctrl+B` | Background current task |
| `Ctrl+T` | Toggle task list |
| `Shift+Tab` | Cycle permission modes |
| `Esc Esc` | Rewind conversation |

### Multiline Input

| Method | Shortcut |
|--------|----------|
| Quick | `\` then `Enter` |
| Mac | `Option+Enter` |
| Alternative | `Ctrl+J` |
| Some terminals | `Shift+Enter` |

### Text Editing (Emacs-style)

| Shortcut | Action |
|----------|--------|
| `Ctrl+K` | Delete to end of line |
| `Ctrl+U` | Delete entire line |
| `Ctrl+Y` | Paste deleted text |
| `Alt+B` | Back one word |
| `Alt+F` | Forward one word |

---

## CLAUDE.md: Your Project Memory

### What Goes in CLAUDE.md

The CLAUDE.md file is loaded every session. Put:

1. **Project commands**: Build, test, deploy commands
2. **Code conventions**: Style guide, patterns to follow
3. **Architecture notes**: How the codebase is organized
4. **Key files**: Important configuration files
5. **Gotchas**: Common mistakes to avoid

### Example CLAUDE.md

```markdown
# Project Guidelines

## Commands
- `npm run dev` - Start dev server (port 3000)
- `npm test` - Run Jest tests
- `npm run lint` - ESLint check
- `npm run build` - Production build

## Code Style
- TypeScript strict mode
- 2-space indentation
- Prefer functional components
- Use React Query for data fetching

## Architecture
- `/src/components` - UI components
- `/src/hooks` - Custom hooks
- `/src/api` - API layer
- `/src/types` - TypeScript types

## Important Files
- `vite.config.ts` - Build config
- `.env.local` - Local environment (never commit)
```

### Memory Locations

| Location | Scope |
|----------|-------|
| `~/.claude/CLAUDE.md` | All your projects |
| `.claude/CLAUDE.md` | This project (shared with team) |
| `./CLAUDE.local.md` | This project (private, .gitignored) |
| `.claude/rules/*.md` | Path-specific rules |

### Use `/init` to Create CLAUDE.md

```
/init
```

Generates a starter template based on your project.

---

## Subagents: Parallel Power

### What Are Subagents?

Subagents are isolated Claude instances that can:
- Work in parallel (research multiple things at once)
- Have specialized knowledge (skills pre-loaded)
- Use isolated context (don't pollute main session)

### Built-in Subagent Types

| Type | Best For |
|------|----------|
| `Explore` | Quick codebase exploration |
| `Plan` | Architecture planning |
| `general-purpose` | Complex multi-step research |

### Example: Parallel Research

```
Research the authentication, database, and API modules in parallel
```

Claude spawns three subagents, each investigating one module, then synthesizes results.

### Creating Custom Subagents

Use `/agents` or create `.claude/agents/my-agent.md`:

```yaml
---
name: code-reviewer
description: "Review code for security and best practices"
version: 1.0.0
model: sonnet
skills:
  - security-checklist
allowed-tools:
  - Read
  - Glob
  - Grep
---

You are a security-focused code reviewer. Check for:
1. Input validation issues
2. SQL injection risks
3. XSS vulnerabilities
4. Authentication weaknesses
```

---

## Skills: Reusable Workflows

### What Are Skills?

Skills are specialized prompts that Claude can invoke. They're like "modes" for specific tasks.

### Finding Skills

```
/                    # Start typing to see available skills
/commit              # Invoke commit skill
/review-pr           # Invoke PR review skill
```

### Creating Custom Skills

Create `.claude/skills/my-skill.md`:

```yaml
---
name: api-design
description: "Design RESTful APIs following best practices"
version: 1.0.0
user-invokable: true
allowed-tools:
  - Read
  - Write
  - Edit
---

# API Design Skill

When designing APIs:
1. Use plural nouns for resources
2. Use HTTP verbs correctly
3. Return appropriate status codes
4. Include pagination for lists
5. Version the API

[More detailed instructions...]
```

### Skill vs Subagent

| Feature | Skill | Subagent |
|---------|-------|----------|
| Context | Main session | Isolated |
| Parallel | No | Yes |
| Persistence | Current turn | Can resume |
| Use case | Specialized mode | Independent research |

---

## MCP Servers: External Integrations

### What is MCP?

Model Context Protocol connects Claude to external tools, databases, and APIs.

### Adding MCP Servers

```bash
# Remote HTTP server (recommended)
claude mcp add --transport http github https://mcp.github.com/mcp

# With authentication
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Local server
claude mcp add airtable -- npx -y airtable-mcp-server
```

### Managing Servers

```bash
claude mcp list              # See all servers
claude mcp list-tools github # See available tools
claude mcp remove github     # Remove server
/mcp                         # In-session management
```

### Popular MCP Servers

| Server | What It Does |
|--------|--------------|
| GitHub | Issues, PRs, repos |
| Notion | Pages, databases |
| Slack | Messages, channels |
| Postgres | Database queries |
| Filesystem | File operations |

---

## Hooks: Automation

### What Are Hooks?

Hooks run shell commands at specific points in Claude's workflow.

### Hook Events

| Event | When |
|-------|------|
| `PreToolUse` | Before tool executes (can block) |
| `PostToolUse` | After tool succeeds |
| `UserPromptSubmit` | Before processing your message |
| `Notification` | Claude sends notification |
| `Stop` | Claude finishes responding |

### Quick Setup

```
/hooks
```

Interactive menu to create hooks.

### Example: Notify When Done

```json
{
  "hooks": {
    "Notification": [{
      "hooks": [{
        "type": "command",
        "command": "notify-send 'Claude needs attention'"
      }]
    }]
  }
}
```

### Example: Auto-Format Code

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "prettier --write $(jq -r '.tool_input.file_path')"
      }]
    }]
  }
}
```

### Example: Block Sensitive Files

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write|Read",
      "hooks": [{
        "type": "command",
        "command": "./check-sensitive-files.sh"
      }]
    }]
  }
}
```

Exit code 2 blocks the action.

---

## Permission Modes

### Available Modes

| Mode | Behavior |
|------|----------|
| `default` | Ask permission per tool type |
| `acceptEdits` | Auto-accept file edits |
| `plan` | Read-only mode |
| `dontAsk` | Auto-deny unless pre-approved |

### Switching Modes

- `Shift+Tab` or `Alt+M` - Cycle modes
- `/plan` - Enter plan mode directly
- `/config` - Change default mode

### Permission Rules

In `settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git *)",
      "Read(./src/**)"
    ],
    "deny": [
      "Read(./.env*)",
      "Bash(rm -rf *)"
    ]
  }
}
```

---

## Git Integration

### Commit Workflow

```
commit my changes
```

Claude:
1. Runs `git status` and `git diff`
2. Analyzes changes
3. Writes descriptive commit message
4. Creates commit

### PR Workflow

```
create a pr
```

Claude:
1. Analyzes all commits since branch
2. Generates PR title and description
3. Creates PR via `gh`

### Worktrees: Parallel Sessions

```
--worktree feature-auth
```

Creates isolated copy of repo with separate branch. No interference between parallel work.

### Session ↔ PR Linking

```bash
claude --from-pr 123   # Resume session linked to PR #123
```

---

## Performance Tips

### Reduce Context Usage

1. **Use `/compact`** before context fills
2. **Create focused skills** instead of huge CLAUDE.md
3. **Delegate to subagents** for verbose operations
4. **Move rules to `.claude/rules/`** for path-specific loading

### Model Selection

| Task | Best Model |
|------|------------|
| Quick exploration | Haiku |
| Most development | Sonnet |
| Complex reasoning | Opus |
| Hard problems | Opus 4.6 (high effort) |

### Monitor Usage

```
/context             # Visual context grid
/cost                # Token spending
/stats               # Usage patterns
```

---

## Power User Workflows

### 1. Research → Plan → Implement

```
1. Ask Claude to research (spawns subagents)
2. /plan to design approach (read-only)
3. Review and approve plan
4. Claude implements
```

### 2. Parallel Feature Development

```bash
# Terminal 1
claude --worktree auth-feature

# Terminal 2
claude --worktree payment-feature

# Each works independently
```

### 3. Automated Code Review

Create a hook that runs on every edit:

```json
{
  "PostToolUse": [{
    "matcher": "Edit",
    "hooks": [{"type": "command", "command": "./run-lint.sh"}]
  }]
}
```

### 4. Session Continuity

```bash
claude --continue              # Resume last session
claude --resume feature-work   # Resume named session
claude --from-pr 456           # Continue PR work
```

---

## Quick Reference Card

### Commands to Remember

```
/clear              # Fresh start
/compact            # Free up context
/model              # Switch models
/plan               # Read-only mode
/resume             # Continue session
/hooks              # Set up automation
/agents             # Create subagents
```

### Shortcuts to Remember

```
Ctrl+O              # Verbose mode
Ctrl+G              # External editor
Ctrl+R              # History search
Ctrl+B              # Background task
Shift+Tab           # Cycle permissions
! command           # Direct bash
@file               # Add to context
```

### Files to Know

```
~/.claude/settings.json       # Your preferences
~/.claude/CLAUDE.md           # Your global memory
.claude/CLAUDE.md             # Project memory
.claude/settings.json         # Project config
.claude/skills/               # Custom skills
.claude/agents/               # Custom agents
```

---

## Getting Help

- `/help` - Built-in help
- `/doctor` - Diagnose issues
- `/debug` - Read debug logs
- https://code.claude.com/docs - Full documentation

---

## Teaching Approach

When users ask about Claude Code:

1. **Assess their level** - Are they new or experienced?
2. **Start with high-impact features** - `!`, `@`, shortcuts
3. **Show, don't tell** - Give examples they can try
4. **Reveal progressively** - Basic → intermediate → advanced
5. **Focus on workflows** - How features combine

### For New Users

Start with:
- `@` mentions for files
- `!` for quick bash
- `/model` for switching
- Basic keyboard shortcuts

### For Intermediate Users

Introduce:
- CLAUDE.md customization
- Subagents for parallel work
- Permission rules
- Session management

### For Power Users

Show:
- Custom skills and agents
- Hooks automation
- MCP server integration
- Worktree workflows
