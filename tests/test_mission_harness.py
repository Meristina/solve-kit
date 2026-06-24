"""End-to-end harness test for the mission loop — no SDK, no network, no API key.

We inject a fake `agents` module into sys.modules BEFORE importing solve_kit.mission
(the package and its officers/soldiers all do `from agents import ...` at import time
and call `.as_tool()` while building the graph). Then we drive `run_mission` by
scripting `Runner.run_sync` outputs and injecting the `approval_fn`, covering the four
control-flow branches: GO->PASS, NO-GO, REVISE->loop, and VETO->iteration cap.
"""

import sys
import types

import pytest

# ---- Stub the openai-agents SDK surface BEFORE importing the package ----------
_fake = types.ModuleType("agents")


class _Agent:
    def __init__(self, *a, **k):
        self.name = k.get("name")
        self.model = k.get("model")
        self.tools = k.get("tools", [])

    def as_tool(self, *a, **k):
        return {"tool_name": k.get("tool_name")}


class _WebSearchTool:
    def __init__(self, *a, **k):
        pass


class _Runner:
    @staticmethod
    def run_sync(agent, inp):  # replaced per-test via ScriptedRunner
        raise RuntimeError("Runner.run_sync not scripted")


_fake.Agent = _Agent
_fake.WebSearchTool = _WebSearchTool
_fake.Runner = _Runner
sys.modules.setdefault("agents", _fake)

from solve_kit import mission  # noqa: E402  (import after stubbing)


class _Result:
    def __init__(self, final_output):
        self.final_output = final_output


class ScriptedRunner:
    """Returns scripted final_outputs in order; records the calls made."""

    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.calls = []

    def run_sync(self, agent, inp):
        self.calls.append(getattr(agent, "name", None))
        return _Result(self.outputs.pop(0))


def _approver(sequence):
    """approval_fn returning (choice, note) from a scripted sequence."""
    seq = iter(sequence)

    def fn(_decision_package):
        return (next(seq), "test")

    return fn


# ---- pure helpers ------------------------------------------------------------

def test_parse_verdict_priority():
    assert mission.parse_verdict("all good, PASS but also VETO on X") == "VETO"
    assert mission.parse_verdict("verdict: PASS WITH FIXES") == "PASS_WITH_FIXES"
    assert mission.parse_verdict("PASS") == "PASS"
    assert mission.parse_verdict("") == "UNCLEAR"


def test_required_fixes_extracted_by_prefix():
    txt = "intro\n- Required: cite the 40% figure\n- Fix: add opt-out\n- nice polish\n- BLOCKING: confirm scope"
    fixes = mission.extract_required_fixes(txt)
    assert len(fixes) == 3


def test_new_dossier_seeds_loop_contract():
    # the keys + defaults the control loop and serializer depend on
    d = mission.new_dossier("p")
    for key in ("problem", "baseline", "hitl", "verdicts", "iteration", "open_to_verify"):
        assert key in d
    assert d["problem"] == "p" and d["iteration"] == 0 and d["hitl"] is None


# ---- the four control-flow branches -----------------------------------------

def test_go_then_pass(monkeypatch):
    # iteration 1: decide -> GO -> execute -> FINAL PASS
    runner = ScriptedRunner(["DECISION PACKAGE", "EXECUTION PLAN", "VERDICT: PASS"])
    monkeypatch.setattr(mission, "Runner", runner)
    d = mission.run_mission("problem", approval_fn=_approver(["GO"]))
    assert "delivered" in d and "stopped" not in d
    assert d["hitl"]["choice"] == "GO"
    assert d["iteration"] == 1
    assert d["verdicts"][-1]["verdict"] == "PASS"


def test_no_go_commits_nothing(monkeypatch):
    # decide -> NO-GO: only one run_sync call, no execution, no verdict
    runner = ScriptedRunner(["DECISION PACKAGE"])
    monkeypatch.setattr(mission, "Runner", runner)
    d = mission.run_mission("problem", approval_fn=_approver(["NO-GO"]))
    assert "stopped" in d and "no resources committed" in d["stopped"].lower()
    assert d["hitl"]["choice"] == "NO-GO"
    assert d["verdicts"] == []          # nothing inspected → no execute/inspect pass ran


def test_revise_then_go(monkeypatch):
    # iter1: decide -> REVISE (loop). iter2: decide -> GO -> execute -> PASS
    runner = ScriptedRunner(["DP1", "DP2", "EXEC", "VERDICT: PASS"])
    monkeypatch.setattr(mission, "Runner", runner)
    d = mission.run_mission("problem", approval_fn=_approver(["REVISE", "GO"]))
    assert d["iteration"] == 2
    assert "delivered" in d
    assert d["hitl"]["choice"] == "GO"


def test_veto_hits_iteration_cap(monkeypatch):
    # every iteration: decide -> GO -> execute -> VETO ; 3 iters -> residual_risk
    outputs = []
    for _ in range(mission.MAX_ITERS):
        outputs += ["DP", "EXEC", "VERDICT: VETO"]
    runner = ScriptedRunner(outputs)
    monkeypatch.setattr(mission, "Runner", runner)
    d = mission.run_mission("problem", approval_fn=_approver(["GO"] * mission.MAX_ITERS))
    assert d["iteration"] == mission.MAX_ITERS
    assert "residual_risk" in d
    assert d["verdicts"][-1]["verdict"] == "VETO"
