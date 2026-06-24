"""Structural invariants — pure file parsing, no imports, no SDK, no network.

Doubles as the durable consistency audit (Workstream 4): wiring completeness,
grade parity (py model= <-> md frontmatter model:), shared-arsenal sanity, counts.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
PKG = ROOT / "solve_kit"
OFFICERS = PKG / "officers"
SOLDIERS = PKG / "soldiers"
SKILLS = ROOT / "skills"

GRADE = {"gpt-5": "opus", "gpt-5-mini": "sonnet"}  # py model -> md model


def _py_model(path: Path) -> str:
    m = re.search(r'model="([^"]+)"', path.read_text(encoding="utf-8"))
    return m.group(1) if m else ""


def _md_model(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("model:"):
            return line.split(":", 1)[1].strip()
    return ""


def _soldier_pys():
    return sorted(p for p in SOLDIERS.glob("soldier_*.py") if p.stem != "__init__")


def _officer_pys():
    return sorted(OFFICERS.glob("officer_*.py"))


# ---- counts -----------------------------------------------------------------

def test_counts():
    assert len(list(AGENTS.glob("soldier-*.md"))) == 24
    assert len(_soldier_pys()) == 24
    assert len(list(AGENTS.glob("officer-*.md"))) == 5
    assert len(_officer_pys()) == 5
    assert len(list(SKILLS.glob("*/SKILL.md"))) == 25  # 24 methods + mission-dossier


# ---- wiring: every soldier is invoked by >=1 officer ------------------------

def test_every_soldier_wired():
    officer_text = "\n".join(p.read_text(encoding="utf-8") for p in _officer_pys())
    for sp in _soldier_pys():
        assert sp.stem in officer_text, f"{sp.stem} is never imported/used by an officer"


# ---- grade parity: py model= <-> md frontmatter model: ----------------------

def _md_for(py: Path) -> Path:
    if py.name == "commander.py":
        return AGENTS / "commander-problem-solving.md"
    if py.name == "inspector.py":
        return AGENTS / "inspector.md"
    return AGENTS / (py.stem.replace("_", "-") + ".md")


def test_grade_parity():
    units = [PKG / "commander.py", PKG / "inspector.py", *_officer_pys(), *_soldier_pys()]
    assert len(units) == 31  # commander + inspector + 5 officers + 24 soldiers
    for py in units:
        md = _md_for(py)
        assert md.exists(), f"no md mirror for {py.name} (looked for {md.name})"
        py_m, md_m = _py_model(py), _md_model(md)
        assert py_m in GRADE, f"{py.name} has unexpected model {py_m!r}"
        assert GRADE[py_m] == md_m, f"grade mismatch {py.name}: py={py_m} md={md_m}"


# ---- shared-arsenal sanity: known shared soldiers used by >=2 officers -------

def test_shared_arsenal():
    texts = {p.name: p.read_text(encoding="utf-8") for p in _officer_pys()}
    for shared in ("soldier_qqoqcp", "soldier_brainstorming", "soldier_mece",
                   "soldier_dashboard", "soldier_check_sheet", "soldier_pareto"):
        used_by = [n for n, t in texts.items() if shared in t]
        assert len(used_by) >= 2, f"{shared} should be shared by >=2 officers, got {used_by}"


# ---- no flat (non-relative) intra-package imports leaked ---------------------

def test_no_flat_imports():
    flat = re.compile(r'^from (commander|inspector|officers|soldiers)\b', re.M)
    for py in PKG.rglob("*.py"):
        assert not flat.search(py.read_text(encoding="utf-8")), f"flat import in {py}"
