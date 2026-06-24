---
description: Final quality gate (Inspector FINAL mode) — sources, compliance, quality; veto
argument-hint: "<mission dir, e.g. missions/001-...>"
---

# /solve.inspect — final gate (Inspector, FINAL mode, veto power)

**Constitution check:** `.solve/memory/constitution.md` (Art. IX). `$MISSION` =
`$ARGUMENTS`.

## Do
1. **Read** all mission artifacts (`dossier.md`, `problem.md`, `causes.md` if any,
   `solution.md`, `actions.md`/`monitor.md` if produced).
2. **Delegate to the `inspector` subagent** (Agent tool — runs on its grade model,
   Opus; else adopt its role inline) in **FINAL mode** — the full pass:
   - **Sources** (Art. I): every fact cites a real internet source; spot-check the
     riskiest by searching. Uncited/hallucinated → automatic VETO until fixed.
   - **Compliance** (Art. II): sector fit; flag where human/expert review is required.
   - **Quality**: devil's-advocate on the weakest points, then **converge** (separate
     fatal flaws from nitpicks).
3. **Verdict**: `PASS` / `PASS WITH FIXES` / `VETO` + the prioritized required fixes
   (each concrete and checkable). Provide evidence for each finding.
4. **Log**: append the verdict + findings to `$MISSION/inspections.md` and the Dossier.

## On PASS-WITH-FIXES / VETO
Fix the **affected** phase only (re-run its command, carry the Dossier) and
**re-inspect**. Loop, capped at `MAX_ITERS=3`; if still failing, deliver the best
result **with residual risk stated** (Art. VII). Mirror the user's language.
