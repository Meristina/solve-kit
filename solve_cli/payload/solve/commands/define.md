---
description: Phase 1 — define AND quantify the right problem (+ baseline)
argument-hint: "<mission dir, e.g. missions/001-...>"
---

# /solve.define — Phase 1 (Officer 1)

**Constitution check:** `.solve/memory/constitution.md` (esp. Art. I sourcing,
Art. VI minimal MECE). `$MISSION` = `$ARGUMENTS` (the mission dir).

## Do
1. **Read in**: `$MISSION/dossier.md` (problem, sector, prior facts) — don't re-ask.
2. **Delegate to the `officer-1-define-problem` subagent** (via the Agent tool, where
   available — it then runs on its own grade model, e.g. Opus on Claude Code; if no
   subagent dispatch is available, adopt the officer's role inline + load its skills):
   produce a sharp, scoped, prioritized problem statement
   **and a measured baseline** of the current state (reuse the `check-sheet` /
   `dashboard` soldiers for the baseline; `qqoqcp` to pin facts; `pareto` to
   prioritize). Pick only the soldiers this case needs.
3. **Fill** `.solve/templates/problem-template.md` → write `$MISSION/problem.md`.
   Baseline = value + when + **source**; if not quantifiable, say so — never fabricate.
4. **Write out**: append to `$MISSION/dossier.md` → set `baseline`, add the decision,
   new assumptions (tagged), sources, and any new à-vérifier item.
5. **Gate**: run `/solve.gate define`. On `GATE: FAIL`, fix `problem.md` and re-gate
   before moving on.

## Done when
`$MISSION/problem.md` exists with a sourced baseline (or an explicit "not
quantifiable"), the Dossier is updated, and `/solve.gate define` returned `GATE: PASS`.
Mirror the user's language.
