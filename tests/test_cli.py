"""CLI tests — offline (no SDK, no network). Exercises `solve init` scaffolding and
the headless dossier serialization. The actual `solve run` engine path needs the SDK
and is covered structurally by test_mission_harness.py."""

from pathlib import Path

from solve_cli import scaffolder, integrations, runner_bridge


def test_init_claude(tmp_path):
    summary = scaffolder.init(str(tmp_path), agent="claude")
    assert (tmp_path / ".solve" / "memory" / "constitution.md").is_file()
    assert (tmp_path / ".solve" / "templates").is_dir()
    assert (tmp_path / "missions").is_dir()
    cmds = list((tmp_path / ".claude" / "commands").glob("solve.*.md"))
    assert len(cmds) == 9, [c.name for c in cmds]
    assert summary["agent"] == "claude"
    assert summary["agents"] == 31 and summary["skills"] == 25


def test_init_cursor_and_copilot(tmp_path):
    s1 = scaffolder.init(str(tmp_path / "cur"), agent="cursor")
    assert len(list((tmp_path / "cur" / ".cursor" / "rules").glob("solve.*.md"))) == 9
    s2 = scaffolder.init(str(tmp_path / "cop"), agent="copilot")
    assert len(list((tmp_path / "cop" / ".github" / "prompts").glob("solve.*.md"))) == 9
    assert s1["agent"] == "cursor" and s2["agent"] == "copilot"


def test_init_rejects_unknown_agent(tmp_path):
    try:
        integrations.install("notanagent", scaffolder.repo_root(), tmp_path)
    except ValueError:
        return
    assert False, "expected ValueError for unknown agent"


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
