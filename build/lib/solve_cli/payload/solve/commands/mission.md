---
description: Start & orchestrate a Solve-Kit mission (the loop) from a problem statement
argument-hint: "<one-line problem>"
---

# /solve.mission — orchestrator (the loop, not the line)

**Constitution check:** read `.solve/memory/constitution.md`. You may not skip
Articles I (sourcing), VIII (HITL before Phase 4), IX (Inspector veto).

## Input
`$ARGUMENTS` = the problem in one line.

## Steps
1. **Scaffold** the mission: run `.solve/scripts/sh/new-mission.sh "$ARGUMENTS"`.
   It prints the mission directory `missions/<NNN-slug>/` and seeds `dossier.md`.
   Use that path as `$MISSION` for everything below.
2. **Select the minimal MECE set** of phases this problem needs (Art. VI); state why
   in one line and record it in `$MISSION/dossier.md` → Decisions.
3. **Drive the phases**, reading the Dossier in and writing it out each time:
   - `/solve.frame` → detect sector, ask 2–3 plan-changing questions, **wait**.
   - `/solve.define` → writes `problem.md` (+ baseline) → then `/solve.gate define`.
   - `/solve.causes` *(if the set needs it)* → `causes.md`.
   - `/solve.design` → writes `solution.md` → then `/solve.gate design`.
4. **HITL checkpoint (Art. VIII):** fill `decision-package.md` from the template,
   present it, and **STOP** for the human: **GO / NO-GO / REVISE**.
   - GO → continue to `/solve.act` then `/solve.monitor` (when those phases are in the set).
   - REVISE → re-run `/solve.design` carrying the Dossier (do not restart from scratch).
   - NO-GO → stop; record in Dossier; commit nothing.
5. **Final gate:** `/solve.inspect` (FINAL) on the assembled deliverable. On VETO /
   PASS-WITH-FIXES, fix the affected phase and re-inspect (loop, cap `MAX_ITERS=3`).

## Done when
`$MISSION/` holds `dossier.md` + the phase artifacts produced, the gates fired after
P1/P3, the HITL decision is recorded, and `inspections.md` carries the final verdict.
Mirror the user's language throughout.
