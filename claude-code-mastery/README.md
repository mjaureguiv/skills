# Claude Code Mastery

Learn to use Claude Code like a power user - discover hidden features, shortcuts, and workflows that 10x your productivity.

## What This Does

Most Claude Code users only scratch the surface. This skill teaches you:
- Hidden keyboard shortcuts that save hours
- Automation with hooks
- Parallel workflows with subagents
- Custom skills for your team
- MCP integrations for external tools

## Quick Wins (Try These Now!)

### 1. Bash Mode with `!`
```
! npm test           # Run directly, no prompts
! git status         # Fast, output added to context
```

### 2. File References with `@`
```
@file.ts             # Add file to context
@src/components/     # Add directory
@file.ts#10-50       # Specific lines only
```

### 3. Essential Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Toggle verbose mode |
| `Ctrl+G` | Open in external editor |
| `Ctrl+R` | Search command history |
| `Ctrl+B` | Background current task |
| `Shift+Tab` | Cycle permission modes |

### 4. Slash Commands
```
/compact             # Free up context space
/model               # Switch between models
/plan                # Enter read-only mode
/resume              # Continue previous session
```

## Topics Covered

### Basics
- Slash commands and what they do
- Keyboard shortcuts cheat sheet
- File and directory references
- Permission modes

### Intermediate
- CLAUDE.md memory files
- Session management
- Git integration (commits, PRs)
- Model selection strategies

### Advanced
- Custom skills and agents
- MCP server integration
- Hooks for automation
- Worktree parallel development
- Performance optimization

## How to Use

Just ask about any Claude Code feature:

```
How do I use subagents in Claude Code?
```

```
What keyboard shortcuts should I know?
```

```
How do I set up automation hooks?
```

```
Teach me Claude Code power user tips
```

## Hidden Features Most People Miss

1. **`!` prefix** - Run bash without asking Claude
2. **`Ctrl+G`** - Edit prompts in your favorite editor
3. **`Ctrl+R`** - Search through command history
4. **`/compact`** - Compress context to continue longer
5. **Worktrees** - Work on multiple features in parallel
6. **Custom hooks** - Auto-format, lint, notify on completion
7. **Subagents** - Spawn parallel research tasks
8. **Skills** - Create reusable specialized prompts

## Quick Reference

### Files
```
~/.claude/CLAUDE.md         # Your global memory
.claude/CLAUDE.md           # Project memory
.claude/settings.json       # Project config
.claude/skills/             # Custom skills
.claude/agents/             # Custom agents
```

### Commands
```
/clear    /compact    /context    /cost
/model    /plan       /resume     /hooks
/agents   /tasks      /vim        /stats
```

### Shortcuts
```
Ctrl+O = verbose      Ctrl+G = editor
Ctrl+R = history      Ctrl+B = background
Ctrl+T = task list    Shift+Tab = mode
```

---

## Resources

- [Official Docs](https://code.claude.com/docs)
- `/help` - Built-in help
- `/doctor` - Diagnose issues

---

*Become a Claude Code power user - ask me anything!*
