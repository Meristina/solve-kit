"""scaffolder — `solve init`: copy the payload into a target project and write the
chosen agent's command files (via integrations).

Resolves the payload from the **repo root** when running from a source checkout
(dev), else from the **bundled** `solve_cli/payload/` shipped in the wheel — so
`solve init` works both in-repo and after `pip install`.
"""

import shutil
from pathlib import Path

from . import integrations


def sources() -> dict:
    """Locate the payload source. Keys: solve, agents, skills, mode."""
    here = Path(__file__).resolve()
    root = here.parents[1]
    if (root / ".solve").is_dir() and (root / "agents").is_dir():
        return {"solve": root / ".solve", "agents": root / "agents",
                "skills": root / "skills", "mode": "source"}
    p = here.parent / "payload"
    if (p / "solve").is_dir():
        return {"solve": p / "solve", "agents": p / "agents",
                "skills": p / "skills", "mode": "bundled"}
    raise RuntimeError("Solve-Kit payload not found — run `solve sync` or reinstall the package.")


def init(target: str, agent: str = "claude") -> dict:
    """Scaffold .solve/ + missions/ into `target` and install the agent command pack."""
    src = sources()
    target = Path(target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    # 1) the .solve/ payload (constitution, templates, commands, scripts)
    shutil.copytree(src["solve"], target / ".solve", dirs_exist_ok=True)

    # 2) missions/ output dir
    (target / "missions").mkdir(exist_ok=True)

    # 3) agent integration (commands + engine)
    summary = integrations.install(agent, src, target)
    summary["target"] = str(target)
    summary["payload_mode"] = src["mode"]
    return summary


def check(target: str = ".") -> list:
    """Lightweight prerequisite/health check. Returns (label, ok, detail) tuples."""
    checks = []
    try:
        src = sources()
        checks.append((f"payload found ({src['mode']})", True, str(src["solve"].parent)))
        checks.append(("constitution present", (src["solve"] / "memory" / "constitution.md").is_file(), ""))
        checks.append(("9 commands present", len(list((src["solve"] / "commands").glob("*.md"))) == 9, ""))
    except RuntimeError as e:
        checks.append(("payload found", False, str(e)))
    try:
        import agents  # noqa: F401  (the openai-agents SDK)
        sdk = True
    except ImportError:
        sdk = False
    checks.append(("openai-agents SDK installed (needed for `solve run`)", sdk, "pip install openai-agents"))
    return checks
