"""runner_bridge — headless mission path.

Calls the UNCHANGED engine `solve_kit.mission.run_mission(..., auto_approve)` and
serializes the returned Mission Dossier dict into `missions/<NNN-slug>/` as Markdown,
so the headless path writes the same on-disk contract as the interactive Claude commands
(`dossier.md` + `deliverable.md`). The rich per-phase artifacts (problem.md, solution.md,
…) are produced by the interactive command path; the headless path captures the carried
Dossier + the final delivered text.
"""

import json
import re
from pathlib import Path


def _slug(text: str, max_words: int = 6) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return "-".join(s.split("-")[:max_words]) or "mission"


def _next_id(missions: Path) -> str:
    nums = []
    if missions.exists():
        for p in missions.iterdir():
            m = re.match(r"(\d{3})-", p.name)
            if m:
                nums.append(int(m.group(1)))
    return f"{(max(nums) + 1) if nums else 1:03d}"


def _dossier_md(mission_id: str, d: dict) -> str:
    """Render the dossier dict as Markdown (mirror of the dossier template)."""
    lines = [f"# Mission Dossier — {mission_id}", ""]
    for key in ("problem", "sector", "baseline", "iteration", "hitl"):
        lines.append(f"- **{key}**: {d.get(key)}")
    lines.append("")
    lines.append("## Assumptions")
    for a in d.get("assumptions", []) or []:
        lines.append(f"- {a}")
    lines.append("\n## Decisions")
    for dec in d.get("decisions", []) or []:
        lines.append(f"- {dec}")
    lines.append("\n## Sources")
    for i, s in enumerate(d.get("sources", []) or [], 1):
        lines.append(f"{i}. {s}")
    lines.append("\n## Open to verify")
    for o in d.get("open_to_verify", []) or []:
        lines.append(f"- {o}")
    lines.append("\n## Verdicts")
    for v in d.get("verdicts", []) or []:
        lines.append(f"- {json.dumps(v, ensure_ascii=False)}")
    if d.get("residual_risk"):
        lines.append(f"\n## Residual risk\n{d['residual_risk']}")
    return "\n".join(lines) + "\n"


def serialize_dossier(dossier: dict, project_root: Path) -> Path:
    """Write the dossier + deliverable into a fresh missions/<NNN-slug>/ folder."""
    project_root = Path(project_root)
    missions = project_root / "missions"
    missions.mkdir(parents=True, exist_ok=True)
    mission_id = f"{_next_id(missions)}-{_slug(dossier.get('problem', ''))}"
    out = missions / mission_id
    out.mkdir()
    (out / "dossier.md").write_text(_dossier_md(mission_id, dossier), encoding="utf-8")
    delivered = dossier.get("delivered") or dossier.get("stopped") or "(no deliverable)"
    (out / "deliverable.md").write_text(
        f"# Deliverable — {mission_id}\n\n{delivered}\n", encoding="utf-8"
    )
    return out


def run(problem: str, project_root: str = ".", auto_approve: bool = True) -> Path:
    """Headless run: drive the engine, then serialize. Needs openai-agents + OPENAI_API_KEY."""
    from solve_kit.mission import run_mission, auto_approve as auto_fn, console_approval

    dossier = run_mission(problem, approval_fn=auto_fn if auto_approve else console_approval)
    return serialize_dossier(dossier, Path(project_root))
