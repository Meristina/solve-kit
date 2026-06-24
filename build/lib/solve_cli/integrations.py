"""integrations — agent adapters. Write the Solve-Kit command pack (single source in
the payload's commands/) into the chosen AI agent's directory, reformatted per agent.

Claude is the reference adapter (commands → /solve.<name>, plus the agents+skills
engine). Cursor / Copilot are provided as thin stubs to be fleshed out.
"""

import shutil
from pathlib import Path

SUPPORTED = ("claude", "cursor", "copilot")


def _copy_commands(src_commands: Path, dest_dir: Path, prefix: str = "solve.") -> int:
    dest_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted(src_commands.glob("*.md")):
        shutil.copyfile(f, dest_dir / f"{prefix}{f.name}")
        n += 1
    return n


def install(agent: str, sources: dict, target: Path) -> dict:
    """Write agent-specific command/engine files into `target`. `sources` from
    scaffolder.sources() (keys: solve, agents, skills). Returns a summary."""
    agent = agent.lower()
    if agent not in SUPPORTED:
        raise ValueError(f"unsupported agent {agent!r}; choose from {SUPPORTED}")

    src_commands = sources["solve"] / "commands"
    target = Path(target)
    summary = {"agent": agent}

    if agent == "claude":
        cmds = _copy_commands(src_commands, target / ".claude" / "commands")
        agents_dir = target / ".claude" / "agents"
        skills_dir = target / ".claude" / "skills"
        agents_dir.mkdir(parents=True, exist_ok=True)
        skills_dir.mkdir(parents=True, exist_ok=True)
        for f in sources["agents"].glob("*.md"):
            shutil.copyfile(f, agents_dir / f.name)
        for d in sources["skills"].iterdir():
            if d.is_dir():
                shutil.copytree(d, skills_dir / d.name, dirs_exist_ok=True)
        summary.update(commands=cmds,
                       agents=len(list(sources["agents"].glob("*.md"))),
                       skills=sum(1 for d in sources["skills"].iterdir() if d.is_dir()))
    elif agent == "cursor":
        cmds = _copy_commands(src_commands, target / ".cursor" / "rules")
        summary.update(commands=cmds, note="cursor: command bodies copied as rules (refine .mdc as needed)")
    elif agent == "copilot":
        cmds = _copy_commands(src_commands, target / ".github" / "prompts")
        summary.update(commands=cmds, note="copilot: command bodies copied as prompts")
    return summary
