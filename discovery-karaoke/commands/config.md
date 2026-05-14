# CMD: config save|show|clear

**Trigger**: `config`

**No subcommand** — STOP. Do not proceed to any subcommand flow. Apply G11 and output only:
> "Available: `config save` | `config show` | `config clear`"

Then wait for the user's next message. Do not ask questions. Do not start the save flow.

---

**config save**:

Ask via AskUserQuestion:
1. Company size: Startup / Scaleup / Enterprise
2. Business model: B2B / B2C / B2B2C / Internal
3. User access: Easy / Moderate / Limited
4. Team size: Solo / Small (2–5) / Cross-functional (5+)
5. Customer base: None / Small / Medium / Large
6. Regulated industry: Yes / No
7. Output mode: Standard (full output by default) / Compact (short summaries by default — use `full` suffix to expand)

Warn if overwriting an existing config (G7).

Write to `.discovery-karaoke-config.yml` in the working directory at time of invocation. On completion, confirm:
> "Config saved to `[resolved path]/.discovery-karaoke-config.yml`. Add this file to `.gitignore` if you don't want team context committed to the repository."

```yaml
# Discovery Karaoke — Team Config
# Saved by /discovery-karaoke config save
# Constraints only. Risk and stage are NOT saved — they change per decision.
team:
  company_size: [value]
  business_model: [value]
  user_access: [value]
  team_size: [value]
  customer_base: [value]
  regulated: [true/false]
  output_mode: [standard|compact]
created: [YYYY-MM-DD]
```

---

**config show**: Read `.discovery-karaoke-config.yml` from the working directory at time of invocation. Display as:
> "Config loaded from: `[resolved path]/.discovery-karaoke-config.yml`"
followed by the config contents in readable format. If none exists:
> "No config found at `[resolved path]/.discovery-karaoke-config.yml`. Run `config save` to create one, or check if you're in the right directory."

---

**config clear**: Confirm before deleting. On confirm: delete `.discovery-karaoke-config.yml`. Note: if you've moved projects, check your previous directory for an orphaned `.discovery-karaoke-config.yml` and remove it manually.
