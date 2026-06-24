"""integrations — agent adapters.

Single source of truth = the payload's `commands/*.md` (YAML frontmatter with
`description` + body using `$ARGUMENTS`). Each adapter transcodes that into the
target agent's native command format:

| agent    | dir                       | file                  | format                         |
|----------|---------------------------|-----------------------|--------------------------------|
| claude   | .claude/commands/         | solve.<n>.md          | MD + frontmatter (as-is)       |
| cursor   | .cursor/commands/         | solve-<n>.md          | MD, NO frontmatter             |
| copilot  | .github/prompts/          | solve-<n>.prompt.md   | YAML frontmatter + body        |
| gemini   | .gemini/commands/solve/   | <n>.toml              | TOML (description + prompt)    |
| opencode | .opencode/commands/       | solve-<n>.md          | MD + frontmatter (description) |

Claude also receives the agents+skills engine (the units the commands drive).
"""

import shutil
from pathlib import Path

SUPPORTED = ("claude", "codex", "cursor", "copilot", "gemini", "opencode")


def _parse_command(path: Path):
    """Return (name, description, body) from a source command markdown file."""
    text = path.read_text(encoding="utf-8")
    name = path.stem  # e.g. "define"
    description, body = "", text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm, body = text[3:end], text[end + 4:].lstrip("\n")
            for line in fm.splitlines():
                if line.strip().startswith("description:"):
                    description = line.split(":", 1)[1].strip().strip('"').strip("'")
                    break
    description = description or f"Solve-Kit /{name}"
    return name, description, body


def _commands(sources: dict):
    for f in sorted((sources["solve"] / "commands").glob("*.md")):
        yield _parse_command(f)


def _write(p: Path, content: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _install_claude(sources, target) -> dict:
    cmds = 0
    for f in sorted((sources["solve"] / "commands").glob("*.md")):
        _write(target / ".claude" / "commands" / f"solve.{f.name}", f.read_text(encoding="utf-8"))
        cmds += 1
    # the engine the commands drive
    for f in sources["agents"].glob("*.md"):
        _write(target / ".claude" / "agents" / f.name, f.read_text(encoding="utf-8"))
    for d in sources["skills"].iterdir():
        if d.is_dir():
            shutil.copytree(d, target / ".claude" / "skills" / d.name, dirs_exist_ok=True)
    return {"commands": cmds,
            "agents": len(list(sources["agents"].glob("*.md"))),
            "skills": sum(1 for d in sources["skills"].iterdir() if d.is_dir())}


def _install_codex(sources, target) -> dict:
    # Codex custom prompts use the SAME format as our source (YAML frontmatter with
    # description/argument-hint + $ARGUMENTS) → near-passthrough copy.
    n = 0
    for f in sorted((sources["solve"] / "commands").glob("*.md")):
        _write(target / ".codex" / "prompts" / f"solve-{f.name}", f.read_text(encoding="utf-8"))
        n += 1
    return {"commands": n,
            "note": "codex: .codex/prompts/solve-*.md → /prompts:solve-<name>. "
                    "Codex reads ~/.codex/prompts/ (home-scoped): copy them there for global use."}


def _install_cursor(sources, target) -> dict:
    n = 0
    for name, _desc, body in _commands(sources):
        _write(target / ".cursor" / "commands" / f"solve-{name}.md", body)  # no frontmatter
        n += 1
    return {"commands": n, "note": "cursor: body-only Markdown in .cursor/commands/ (no frontmatter)"}


def _install_copilot(sources, target) -> dict:
    n = 0
    for name, desc, body in _commands(sources):
        content = f"---\ndescription: {desc}\nmode: agent\n---\n\n{body}"
        _write(target / ".github" / "prompts" / f"solve-{name}.prompt.md", content)
        n += 1
    return {"commands": n, "note": "copilot: .github/prompts/*.prompt.md (mode: agent)"}


def _toml_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')


def _install_gemini(sources, target) -> dict:
    n = 0
    for name, desc, body in _commands(sources):
        prompt = _toml_escape(body).replace("$ARGUMENTS", "{{args}}")
        content = f'description = "{desc}"\nprompt = """\n{prompt}\n"""\n'
        _write(target / ".gemini" / "commands" / "solve" / f"{name}.toml", content)
        n += 1
    return {"commands": n, "note": "gemini: .gemini/commands/solve/*.toml → /solve:<name> (args {{args}})"}


def _install_opencode(sources, target) -> dict:
    n = 0
    for name, desc, body in _commands(sources):
        content = f"---\ndescription: {desc}\n---\n\n{body}"
        _write(target / ".opencode" / "commands" / f"solve-{name}.md", content)
        n += 1
    return {"commands": n, "note": "opencode: .opencode/commands/solve-*.md ($ARGUMENTS supported)"}


_ADAPTERS = {
    "claude": _install_claude,
    "codex": _install_codex,
    "cursor": _install_cursor,
    "copilot": _install_copilot,
    "gemini": _install_gemini,
    "opencode": _install_opencode,
}


def install(agent: str, sources: dict, target: Path) -> dict:
    """Write agent-specific command/engine files into `target`. Returns a summary."""
    agent = agent.lower()
    if agent not in _ADAPTERS:
        raise ValueError(f"unsupported agent {agent!r}; choose from {SUPPORTED}")
    summary = {"agent": agent}
    summary.update(_ADAPTERS[agent](sources, Path(target)))
    return summary
