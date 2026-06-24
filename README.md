# Solve-Kit

A **generalist, sector-agnostic problem-solving agent army**, portable across
**Claude** (`agents/` + `skills/`) and **OpenAI** (the `solve_kit/` Python package).
Give it any real problem; it runs a disciplined methodology to a sourced, gated,
human-approved result.

## The doctrine — five phases
```
Commander → Officer 1 Define + baseline → Officer 2 Causes → Officer 3 Solution
          → Officer 4 Actions → Officer 5 Monitor      (+ transverse Inspector, veto)
```
1. **Define & quantify** the *right* problem (+ a measured baseline).
2. **Identify root causes** (not symptoms).
3. **Design the solution** (generate → compare → choose, with trade-offs).
4. **Launch the actions** (owners, critical path, risks).
5. **Monitor effectiveness** (KPIs vs the baseline, steer).

Cross-cutting guarantees: **no invented information** (every fact internet-sourced or
flagged), a **Mission Dossier** carrying state across phases, **quick quality gates**
after Phase 1 and Phase 3, a **human GO/NO-GO/REVISE checkpoint** before committing
resources (Phase 4), and a final **Inspector veto** (sources · compliance · quality).
The runner loops (DECIDE → HITL → EXECUTE → FINAL-inspect → re-enter) up to `MAX_ITERS`.

## Two runtimes

### Claude
Copy the agents and skills into your Claude config, then talk to the commander:
```bash
mkdir -p ~/.claude/agents ~/.claude/skills
cp agents/*.md   ~/.claude/agents/
cp -R skills/*   ~/.claude/skills/
```

### OpenAI (Python package)
```bash
pip install -e .                      # installs the `solve-kit` package
solve-kit-mission "Describe your problem here"
# or:
python -m solve_kit.mission "Describe your problem here"
```
Requires `openai-agents` and `OPENAI_API_KEY`. Every unit has hosted web search, so
no unit invents facts. The interactive run pauses at the human GO/NO-GO/REVISE gate;
for headless runs, call `solve_kit.mission.run_mission(problem, approval_fn=auto_approve)`.

### CLI — scaffold into any project, any agent
```bash
solve init <project> --agent <claude|cursor|copilot|gemini|opencode>
solve run "<problem>" --auto-approve      # headless, writes missions/<NNN>/
solve check                               # health/prereqs
```
`solve init` writes the `/solve.*` command pack into the chosen agent's native format
(Claude `.claude/commands/`, Cursor `.cursor/commands/`, Copilot `.github/prompts/`,
Gemini `.gemini/commands/solve/*.toml`, opencode `.opencode/commands/`) — single source
in `.solve/commands/`, transcoded per agent.

## Architecture
- `solve_kit/` — the OpenAI engine: `commander.py`, `inspector.py`, `mission.py`
  (the deterministic loop + HITL runner), `officers/` (5), `soldiers/` (24).
- `agents/` — the Claude mirror (commander, inspector, 5 officers, 24 soldiers).
- `skills/` — 25 method procedures (24 methods + `mission-dossier`); also the source
  of the toolkit templates.
- `tests/` — structural audit + a no-network harness test (stubs the SDK).

## Grades
🔵 standard (`sonnet` / `gpt-5-mini`) vs 🎖️ elite (`opus` / `gpt-5`). The elite
criterion is **depth of reasoning**, not method fame.

## More
- **`GUIDE.md`** — full usage manual, the 24-method catalogue, install, and the
  repeatable pattern to add a soldier.
