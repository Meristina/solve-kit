"""
MISSION RUNNER — deterministic control loop + Mission Dossier + HITL gate (OpenAI port)

The army's spine. Where commander.py *defines* the commander agent, this runner
*drives the mission*: it holds the Mission Dossier (living state), runs the army in
two stages with a HUMAN go/no-go gate between them, runs the Inspector, parses the
verdict, and controls re-entry and the iteration cap. The commander agent is the
brain within a pass; this harness owns the loop — see agents/commander-problem-
solving.md ("Control loop", "HITL CHECKPOINT") and the `mission-dossier` skill.

Two stages per iteration:
  DECIDE   (Phases 0-3: frame -> define+baseline -> causes -> solution)
  --- HITL gate: human GO / NO-GO / REVISE before any resources are committed ---
  EXECUTE  (Phases 4-5: launch actions -> monitor)  [only on GO]
Then the FINAL Inspector verdict gates delivery.

Run:  cd openai && python mission.py "Describe the problem here"
(Requires `pip install openai-agents` and OPENAI_API_KEY.)
"""

import json
import sys

from agents import Runner

from .commander import commander
from .inspector import inspector

MAX_ITERS = 3  # iteration cap — deliver-with-residual-risk rather than thrash forever


def new_dossier(problem: str) -> dict:
    """The single living-state artifact carried across the whole mission."""
    return {
        "problem": problem,
        "sector": None,
        "baseline": None,          # measured current state (set in Phase 1)
        "assumptions": [],
        "decisions": [],
        "sources": [],
        "open_to_verify": [],
        "hitl": None,              # the human go/no-go decision before Phase 4
        "verdicts": [],            # Inspector verdicts + required fixes, per iteration
        "iteration": 0,
    }


def _dossier_block(dossier: dict) -> str:
    return json.dumps(dossier, ensure_ascii=False, indent=2)


def decide_brief(dossier: dict, required_fixes: list) -> str:
    """Stage 1 — run Phases 0-3 and STOP at the HITL checkpoint with a decision package."""
    parts = [
        "MISSION DOSSIER (read in; do not re-ask what is already here):",
        _dossier_block(dossier),
        "\nRun PHASES 0-3 ONLY: frame, define + baseline (Officer 1), root causes "
        "(Officer 2), design & choose the solution (Officer 3) — with the quick GATE "
        "checks after Phase 1 and Phase 3. STOP at the HITL checkpoint; do NOT start "
        "Phase 4.",
        "\nReturn a DECISION PACKAGE in the user's language: the chosen solution + why, "
        "what Phase 4 would commit (resources/budget/effort), the expected timeline, "
        "and the top risks. Make sources and open à-vérifier items explicit.",
    ]
    if required_fixes:
        parts.append(
            "\nRE-ENTRY — resolve these before re-presenting (carry the dossier):\n- "
            + "\n- ".join(required_fixes)
        )
    return "\n".join(parts)


def execute_brief(dossier: dict, decision_package: str) -> str:
    """Stage 2 — the human approved; run Phases 4-5 on top of the decision."""
    return "\n".join([
        "MISSION DOSSIER:",
        _dossier_block(dossier),
        "\nThe human APPROVED the decision below. Run PHASES 4-5: launch the actions "
        "(Officer 4 — action plan, critical path, risks) then monitoring (Officer 5).",
        "\nAPPROVED DECISION:\n" + decision_package,
        "\nReturn the full deliverable in the user's language: the decision recap, the "
        "action plan (owners/dates), the critical path, and the monitoring setup, with "
        "sources and open à-vérifier items explicit.",
    ])


def parse_verdict(text: str) -> str:
    """Map the Inspector's free text to a machine verdict. Order matters (VETO first)."""
    upper = (text or "").upper()
    if "VETO" in upper:
        return "VETO"
    if "PASS WITH FIXES" in upper or "PASS-WITH-FIXES" in upper:
        return "PASS_WITH_FIXES"
    if "PASS" in upper:
        return "PASS"
    return "UNCLEAR"


def extract_required_fixes(text: str) -> list:
    """Best-effort pull of the required-fix bullet lines from the Inspector output."""
    fixes = []
    for line in (text or "").splitlines():
        s = line.strip().lstrip("-*•").strip()
        if s and any(s.upper().startswith(p) for p in ("FIX", "REQUIRED", "BLOCK")):
            fixes.append(s)
    return fixes


# ----- HITL approval functions (injectable) ---------------------------------------

def console_approval(decision_package: str) -> tuple:
    """Default human gate: show the decision package, read GO / NO-GO / REVISE."""
    print("\n=== HUMAN CHECKPOINT — approve BEFORE committing resources (Phase 4) ===")
    print(decision_package)
    raw = input("\nApprove? [GO / NO-GO / REVISE]: ").strip().lower()
    note = input("Note (optional): ").strip()
    if raw in ("go", "g", "yes", "y", "oui", "o"):
        return ("GO", note)
    if raw in ("revise", "r"):
        return ("REVISE", note)
    return ("NO-GO", note)  # default to the safe choice: don't commit


def auto_approve(decision_package: str) -> tuple:
    """Non-interactive gate (tests / headless): always GO, clearly labeled."""
    return ("GO", "auto-approved (non-interactive run)")


# ----- The mission loop -----------------------------------------------------------

def run_mission(problem: str, approval_fn=console_approval) -> dict:
    """Drive the full loop with a human gate before execution. Returns the dossier."""
    dossier = new_dossier(problem)
    required_fixes: list = []
    deliverable = ""

    while dossier["iteration"] < MAX_ITERS:
        dossier["iteration"] += 1
        print(f"\n=== ITERATION {dossier['iteration']}/{MAX_ITERS} ===")

        # STAGE 1 — DECIDE (Phases 0-3). The commander stops at the HITL checkpoint.
        decision = Runner.run_sync(commander, decide_brief(dossier, required_fixes))
        decision_package = decision.final_output

        # HITL gate — human authority to spend (distinct from the Inspector's quality gate).
        choice, note = approval_fn(decision_package)
        dossier["hitl"] = {"iteration": dossier["iteration"], "choice": choice, "note": note}
        print(f"Human checkpoint: {choice}" + (f" — {note}" if note else ""))

        if choice == "NO-GO":
            dossier["delivered"] = decision_package
            dossier["stopped"] = "Human NO-GO before Phase 4 — no resources committed. " + note
            return dossier
        if choice == "REVISE":
            required_fixes = ["Human REVISE before Phase 4: " + (note or "revise the solution")]
            continue  # loop back to the decide stage with the human's steer

        # STAGE 2 — EXECUTE (Phases 4-5), only after GO.
        execution = Runner.run_sync(commander, execute_brief(dossier, decision_package))
        deliverable = decision_package + "\n\n---\n\n" + execution.final_output

        # FINAL Inspector verdict of record (the harness owns it).
        inspection = Runner.run_sync(
            inspector,
            "MODE: FINAL. Inspect this deliverable (sources / compliance / quality) and "
            "end with a clear verdict line — PASS, PASS WITH FIXES, or VETO — plus the "
            "required fixes as bullet lines:\n\n" + deliverable,
        )
        verdict = parse_verdict(inspection.final_output)
        required_fixes = extract_required_fixes(inspection.final_output)
        dossier["verdicts"].append({
            "iteration": dossier["iteration"],
            "verdict": verdict,
            "required_fixes": required_fixes,
        })
        print(f"Inspector verdict: {verdict}  ({len(required_fixes)} required fix(es))")

        if verdict == "PASS":
            dossier["delivered"] = deliverable
            return dossier
        # else loop with the fixes carried in the dossier.

    # Iteration cap reached: deliver best result WITH residual risk stated.
    dossier["delivered"] = deliverable
    dossier["residual_risk"] = (
        "Iteration cap reached without a clean PASS. Delivered the best result; "
        f"unresolved required fixes: {required_fixes}; open_to_verify: {dossier['open_to_verify']}."
    )
    return dossier


def main() -> None:
    """Console-script entry point (`solve-kit-mission "<problem>"`)."""
    problem = sys.argv[1] if len(sys.argv) > 1 else "We have a problem: ... (describe it)"
    final = run_mission(problem)  # interactive human gate by default
    print("\n=== DELIVERED ===")
    print(final.get("delivered", "(nothing)"))
    if final.get("stopped"):
        print("\n=== STOPPED ===")
        print(final["stopped"])
    if final.get("residual_risk"):
        print("\n=== RESIDUAL RISK ===")
        print(final["residual_risk"])


if __name__ == "__main__":
    main()
