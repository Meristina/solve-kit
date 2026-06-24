---
description: Phase 2 — identify the true root causes (not symptoms)
argument-hint: "<mission dir, e.g. missions/001-...>"
---

# /solve.causes — Phase 2 (Officer 2)

**Constitution check:** `.solve/memory/constitution.md` (Art. I sourcing, Art. VI
minimal MECE). `$MISSION` = `$ARGUMENTS`.

## Do
1. **Read in**: `$MISSION/problem.md` (+ baseline) and `$MISSION/dossier.md`.
2. **Delegate to the `officer-2-root-cause` subagent** (Agent tool — runs on its grade
   model; else adopt its role inline): get to
   true causes with the minimal set of soldiers — Ishikawa (5M), 5-Whys, relations
   diagram, MECE. Rank causes; flag the **driving** ones; keep the set MECE.
3. **Fill** `.solve/templates/causes-template.md` → write `$MISSION/causes.md`. Every
   factual claim sourced or tagged `à vérifier`.
4. **Write out**: append the ranked causes (decision), sources, à-vérifier to
   `$MISSION/dossier.md`.

## Done when
`$MISSION/causes.md` lists ranked, evidenced root causes with a MECE check, and the
Dossier is updated. (No quick gate here — gates fire after P1 and P3.) Mirror the
user's language.
