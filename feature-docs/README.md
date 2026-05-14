# feature-docs

Generate professional user-facing documentation for product features from Jira epics.

## What This Does

Transforms feature specifications into clear, benefit-focused documentation:
- **Feature Documentation** - Complete docs for new capabilities
- **Incremental Updates** - What changed and why it matters
- **Migration Guides** - Step-by-step guides for breaking changes

Integrates with Jira to pull context automatically.

## Why This Exists

User documentation should be:
- Focused on what users can accomplish (not technical details)
- Consistent in voice and structure
- Connected to real examples
- Ready to publish without heavy editing

This skill automates the mindless parts of documentation writing.

## Usage

### From a Jira Epic

```
/feature-docs SIG-1234
```

Or with more context:

```
/feature-docs
Epic: SIG-1234
Type: Feature documentation
Audience: Admins
```

### From Scratch

```
/feature-docs
We added a new feature that lets users filter processes by lifecycle status.
Users can now see which processes are draft, active, or archived from the list view.
```

## Output Format

Documentation follows structured templates:

### Feature Documentation
```markdown
# {Feature Title}
{1-2 sentence overview}

## How {Feature} Works
{User-focused explanation}

## Best Practice: {Recommended Approach}
{Concrete example}

## Why This Matters
{User benefits}

## Related Resources
{Links to related docs}
```

### Incremental Update
```markdown
# {Feature}: {Change Description}

## What Changed
**Previously:** {old behavior}
**Now:** {new behavior}

## Impact on Your Workflow
{Action required or not}
```

## Documentation Types

| Type | Use When |
|------|----------|
| Feature Documentation | New capability or feature launch |
| Incremental Update | Enhancement to existing functionality |
| Migration Guide | Breaking changes requiring user action |

## Writing Guidelines

The skill enforces:
- **Neutral tone** - Inform, don't sell
- **User focus** - Benefits over technical details
- **Concrete examples** - Real scenarios with real values
- **No marketing language** - Skip "exciting" and "powerful"
- **Consistent terminology** - Uses exact product names

## Jira Integration

When connected to Jira:
- Pulls epic details, acceptance criteria, and linked issues
- Uses summary and description as starting point

Works without Jira - just provide feature details manually.

## Templates Included

- `templates/feature-docs.md` - New feature documentation
- `templates/incremental-update.md` - Feature updates
- `templates/migration-guide.md` - Breaking changes

## Related Skills

- `powerpoint` - Turn docs into presentation slides
- `transcript-to-notes` - Extract feature discussions from meetings

## Support

Questions or issues? Reach out in #claude-code-help

---

**Original Author**: Aviral Vaid (LeanIX Product Management)
**Category**: Workflow
**Integrated from**: [LeanIX PM Marketplace](https://github.tools.sap/LeanIX/LeanIX-PM-Marketplace)
