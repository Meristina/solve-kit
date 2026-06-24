"""scaffolder — `solve init`: copy the .solve/ payload into a target project and write
the chosen agent's command files (via integrations)."""

import shutil
from pathlib import Path

from . import integrations


def repo_root() -> Path:
    """The Solve-Kit source repo (parent of this package) — the payload source of truth."""
    return Path(__file__).resolve().parents[1]


def init(target: str, agent: str = "claude") -> dict:
    """Scaffold .solve/ + missions/ into `target` and install the agent command pack."""
    root = repo_root()
    target = Path(target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    # 1) the .solve/ payload (constitution, templates, commands, scripts)
    src_solve = root / ".solve"
    dst_solve = target / ".solve"
    shutil.copytree(src_solve, dst_solve, dirs_exist_ok=True)

    # 2) missions/ output dir
    (target / "missions").mkdir(exist_ok=True)

    # 3) agent integration (commands + engine)
    summary = integrations.install(agent, root, target)
    summary["target"] = str(target)
    summary["solve_payload"] = str(dst_solve)
    return summary


def check(target: str = ".") -> list:
    """Lightweight prerequisite/health check. Returns a list of (label, ok, detail)."""
    target = Path(target).resolve()
    root = repo_root()
    checks = []
    checks.append((".solve payload present in repo", (root / ".solve").is_dir(), str(root / ".solve")))
    checks.append(("constitution present", (root / ".solve" / "memory" / "constitution.md").is_file(), ""))
    checks.append(("9 commands present", len(list((root / ".solve" / "commands").glob("*.md"))) == 9, ""))
    try:
        import agents  # noqa: F401  (the openai-agents SDK)
        sdk = True
    except Exception:
        sdk = False
    checks.append(("openai-agents SDK installed (needed for `solve run`)", sdk, "pip install openai-agents"))
    return checks
