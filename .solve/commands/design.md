---
description: Phase 3 — generate options, compare on weighted criteria, choose
argument-hint: "<mission dir, e.g. missions/001-...>"
---

# /solve.design — Phase 3 (Officer 3)

**Constitution check:** `.solve/memory/constitution.md` (Art. I sourcing, Art. VI
minimal MECE). `$MISSION` = `$ARGUMENTS`.

## Do
1. **Read in**: `$MISSION/dossier.md` and `$MISSION/causes.md` if present, else
   `$MISSION/problem.md` (the driving causes / the problem to solve).
2. **Invoke Officer 3** (`agents/officer-3-solution.md`, or adopt its role): diverge
   (e.g. brainstorming / scamper / asit) to generate options, then converge with the
   **decision-matrix** soldier — weights fixed BEFORE scoring, knock-outs first,
   consistent scale, weighted totals, and a **sensitivity** check. Trade-offs visible.
3. **Fill** `.solve/templates/solution-template.md` → write `$MISSION/solution.md`.
   Factual scores cite a source; judgment scores labeled as estimates (Art. I).
4. **Write out**: append the chosen option + why (decision), runner-up, sources, and
   à-vérifier items to `$MISSION/dossier.md`.
5. **Gate**: run `/solve.gate design`. On `GATE: FAIL`, fix and re-gate.

## Next
After the gate passes, the orchestrator produces `decision-package.md` and **stops at
the HITL GO/NO-GO/REVISE checkpoint** (Art. VIII) before any Phase-4 action.

## Done when
`$MISSION/solution.md` has a real weighted matrix + sensitivity verdict +
recommendation, the Dossier is updated, and `/solve.gate design` returned `GATE: PASS`.
Mirror the user's language.
