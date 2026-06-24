---
description: Phase 4 — turn the chosen solution into an owned, scheduled, risk-managed plan (requires HITL GO)
argument-hint: "<mission dir, e.g. missions/001-...>"
---

# /solve.act — Phase 4 (Officer 4)

**Constitution check:** `.solve/memory/constitution.md` — **Art. VIII is binding**.
`$MISSION` = `$ARGUMENTS`.

## HARD PRECONDITION (Art. VIII)
Read `$MISSION/dossier.md` → `hitl`. **If `hitl` is not `GO`, REFUSE** and stop:
> "Phase 4 commits resources and requires a human GO. Run `/solve.design`, then approve
> the decision package (GO) before `/solve.act`."
Only proceed when `hitl: GO` is recorded.

## Do
1. **Read in**: `$MISSION/solution.md`, `$MISSION/decision-package.md`, `dossier.md`.
2. **Delegate to the `officer-4-launch-actions` subagent** (Agent tool — runs on its
   grade model; else adopt its role inline):
   PLAN (action-plan: owner/resources/deadline/success-criterion/deps — **no status
   field**) → SCHEDULE (PERT critical path, Gantt) → SECURE (risk-raid register).
3. **Fill** `.solve/templates/actions-template.md` → write `$MISSION/actions.md`.
   Dates/costs sourced or flagged; never a date without an owner and a success test.
4. **Write out**: append the plan summary + top risks (decision) + sources to `dossier.md`.

## Done when
`$MISSION/actions.md` has the action plan (owners/dates), the critical path, and the
RAID register — and it ran **only because `hitl: GO`**. Mirror the user's language.
