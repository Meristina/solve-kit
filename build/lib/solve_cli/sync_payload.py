"""sync_payload — regenerate the bundled payload from the root source of truth.

The repo root holds the canonical `.solve/`, `agents/`, `skills/` (dev + Claude `cp`
install). To make a pip-installed wheel self-contained (so `solve init` works without
the cloned repo), those dirs are mirrored under `solve_cli/payload/` (committed, so
`pip install git+…` and wheels carry them). Dot-dirs are avoided in the bundle:
`.solve` → `payload/solve`. A drift test asserts the mirror stays byte-identical
(Constitution Art. IV — no silent duplication).

Run:  solve sync   (or: python -m solve_cli.sync_payload)
"""

import shutil
from pathlib import Path

# (root source dir, bundled name under solve_cli/payload/)
MAP = [(".solve", "solve"), ("agents", "agents"), ("skills", "skills")]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def payload_dir() -> Path:
    return Path(__file__).resolve().parent / "payload"


def sync() -> dict:
    root, dest = repo_root(), payload_dir()
    summary = {}
    for src_name, bundle_name in MAP:
        src = root / src_name
        dst = dest / bundle_name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        summary[bundle_name] = sum(1 for _ in dst.rglob("*") if _.is_file())
    return summary


def main() -> int:
    s = sync()
    print(f"Synced payload → {payload_dir()}")
    for k, n in s.items():
        print(f"  {k:<8} {n} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
