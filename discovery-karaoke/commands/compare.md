# CMD: compare [M##] vs [M##]

**Trigger**: `compare`

**Data files**:
- `data/methods-index.md` — metadata for the side-by-side overview table (Risk, Stage, Time, Effort, Cost, Evidence, Needs Users)
- `data/discovery-methods-full.md` — prose content for "When to Choose Each" and Karaoke Check sections
- `templates/comparison-template.md`

**Parse**: Extract two M-codes from the remaining argument. Accept: `M1 vs M23`, `M1 M23`, `M1 and M23`.

**Fewer than 2 IDs**: Apply G11:
> "Specify two M-codes. Example: `/discovery-karaoke compare M1 vs M23`
> Not sure which methods to compare? `/discovery-karaoke list methods [filter]`"

**Step 1**: Read both entries from `data/methods-index.md` to build the side-by-side metadata table. Then read both full entries from `data/discovery-methods-full.md` for the "When to Choose Each" and Karaoke Check prose.

**Step 2**: Check output_mode (config or `full` suffix). Read `templates/comparison-template.md`. Deliver output using the Compact Template if output_mode is `compact`, Full Template if `standard` or `full` suffix was used.

**Step 3 — Constrained default** *(after delivering the card)*:
If a saved config exists (`.discovery-karaoke-config.yml`) or constraints are clearly inferable from the situation context, add a single closing line:
> "Under [constraint], start with [M##]."
Frame as a default for the given context, not a winner. Omit this line entirely if no constraints are available — do not guess.

**Rules (always apply)**:
- Never declare a winner without context — always frame as "depends on your risk and constraints" (G2)
- Always show when to use each AND when to use both in sequence
- Always surface the named karaoke risk for each method (G6)
