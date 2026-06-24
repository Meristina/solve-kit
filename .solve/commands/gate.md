---
description: Quick inter-phase quality gate (Inspector GATE mode) on one phase
argument-hint: "<phase: define | design> [mission dir]"
---

# /solve.gate — quick gate (Inspector, GATE mode)

**Constitution check:** `.solve/memory/constitution.md` (Art. IX). `$ARGUMENTS` names
the phase (`define` or `design`) and optionally the mission dir.

## Do
1. **Read** the phase artifact (`problem.md` for `define`, `solution.md` for `design`)
   and `dossier.md`.
2. **Invoke the Inspector** (`agents/inspector.md`) in **GATE mode** — check ONLY:
   - is the phase's **definition of done** met (complete for the phase)?
   - any **unsourced fact / fabricated number / invented citation**? (Art. I)
   Keep it cheap — no full compliance sweep, no deep devil's-advocate here.
3. **Return** `GATE: PASS` or `GATE: FAIL` + the 1–3 must-fix items.
4. **Log**: append the verdict to `$MISSION/inspections.md` and the Dossier → Verdicts.

## On FAIL
Do not proceed. Re-run the phase command (`/solve.define` or `/solve.design`) to fix
the must-fix items, carrying the Dossier, then re-gate. A weak phase must not poison
the downstream.
