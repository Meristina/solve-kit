"""CLI tests — offline (no SDK, no network). Exercises `solve init` scaffolding and
the headless dossier serialization. The actual `solve run` engine path needs the SDK
and is covered structurally by test_mission_harness.py."""

from pathlib import Path

import filecmp

from solve_cli import scaffolder, integrations, runner_bridge, sync_payload
from solve_cli import cli


def test_cli_main_init(tmp_path, capsys):
    """Exercise the full CLI layer (argparse + _cmd_init print path), not just scaffolder."""
    rc = cli.main(["init", str(tmp_path), "--agent", "claude"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Initialized Solve-Kit" in out and "payload source" in out
    assert (tmp_path / ".claude" / "commands").is_dir()


def test_cli_main_check(tmp_path):
    assert cli.main(["check", str(tmp_path)]) in (0, 1)  # returns status, shouldn't raise


def test_init_claude(tmp_path):
    summary = scaffolder.init(str(tmp_path), agent="claude")
    assert (tmp_path / ".solve" / "memory" / "constitution.md").is_file()
    assert (tmp_path / ".solve" / "templates").is_dir()
    assert (tmp_path / "missions").is_dir()
    cmds = list((tmp_path / ".claude" / "commands").glob("solve.*.md"))
    assert len(cmds) == 9, [c.name for c in cmds]
    assert summary["agent"] == "claude"
    assert summary["agents"] == 31 and summary["skills"] == 25


def test_init_all_agents(tmp_path):
    expected = {
        "codex":    (".codex/prompts", "solve-define.md", 9),
        "cursor":   (".cursor/commands", "solve-define.md", 9),
        "copilot":  (".github/prompts", "solve-define.prompt.md", 9),
        "gemini":   (".gemini/commands/solve", "define.toml", 9),
        "opencode": (".opencode/commands", "solve-define.md", 9),
    }
    for agent, (subdir, sample, count) in expected.items():
        proj = tmp_path / agent
        s = scaffolder.init(str(proj), agent=agent)
        files = list((proj / subdir).glob("*"))
        assert len(files) == count, (agent, [f.name for f in files])
        assert (proj / subdir / sample).is_file(), (agent, sample)
        assert s["agent"] == agent


def test_transcoding_specifics(tmp_path):
    # cursor: no YAML frontmatter in the body
    scaffolder.init(str(tmp_path / "cur"), agent="cursor")
    cur = (tmp_path / "cur" / ".cursor" / "commands" / "solve-define.md").read_text()
    assert not cur.startswith("---"), "cursor commands must not carry frontmatter"
    # copilot: agent-mode frontmatter
    scaffolder.init(str(tmp_path / "cop"), agent="copilot")
    cop = (tmp_path / "cop" / ".github" / "prompts" / "solve-define.prompt.md").read_text()
    assert cop.startswith("---") and "mode: agent" in cop
    # gemini: TOML with description + prompt, args rewritten to {{args}}
    scaffolder.init(str(tmp_path / "gem"), agent="gemini")
    gem = (tmp_path / "gem" / ".gemini" / "commands" / "solve" / "define.toml").read_text()
    assert "description =" in gem and 'prompt = """' in gem
    assert "$ARGUMENTS" not in gem and "{{args}}" in gem


def test_init_rejects_unknown_agent(tmp_path):
    try:
        integrations.install("notanagent", scaffolder.sources(), tmp_path)
    except ValueError:
        return
    assert False, "expected ValueError for unknown agent"


def test_bundled_payload_in_sync():
    """Drift guard (Constitution Art. IV): the bundled payload must byte-match the
    root source of truth. If this fails, run `solve sync` and commit."""
    root = sync_payload.repo_root()
    payload = sync_payload.payload_dir()
    for src_name, bundle_name in sync_payload.MAP:
        src, dst = root / src_name, payload / bundle_name
        assert dst.is_dir(), f"bundled {bundle_name} missing — run `solve sync`"
        cmp = filecmp.dircmp(src, dst)
        drift = cmp.left_only + cmp.right_only + cmp.diff_files
        # recurse one level for subdirs (skills/*/, .solve/*/)
        for sub in cmp.common_dirs:
            sc = filecmp.dircmp(src / sub, dst / sub)
            drift += [f"{sub}/{x}" for x in sc.left_only + sc.right_only + sc.diff_files]
        assert not drift, f"payload drift in {bundle_name}: {drift} — run `solve sync`"


def test_serialize_dossier(tmp_path):
    dossier = {
        "problem": "Checkout abandonment rose to 79% in Q2",
        "sector": "e-commerce",
        "baseline": "79% (Q2, analytics)",
        "iteration": 1,
        "hitl": "GO",
        "assumptions": ["x — confirmed"],
        "decisions": [{"phase": "design", "choice": "O4"}],
        "sources": ["https://example.com/a"],
        "open_to_verify": ["targeting"],
        "verdicts": [{"iteration": 1, "verdict": "PASS"}],
        "delivered": "The recommendation is ...",
    }
    out = runner_bridge.serialize_dossier(dossier, tmp_path)
    assert out.name.startswith("001-checkout")
    dm = (out / "dossier.md").read_text(encoding="utf-8")
    assert "Checkout abandonment" in dm and "GO" in dm and "PASS" in dm
    assert "The recommendation is" in (out / "deliverable.md").read_text(encoding="utf-8")


def test_check_payload(tmp_path):
    results = {label: ok for label, ok, _ in scaffolder.check(str(tmp_path))}
    assert all(ok for label, ok in results.items() if "SDK" not in label)
