"""solve — Solve-Kit CLI. Subcommands: init, run, check, version."""

import argparse
import sys

from . import __version__, scaffolder


def _cmd_init(args) -> int:
    summary = scaffolder.init(args.path, agent=args.agent)
    print(f"Initialized Solve-Kit in {summary['target']} (agent: {summary['agent']})")
    print(f"  .solve/ payload : {summary['solve_payload']}")
    if "commands" in summary:
        print(f"  commands       : {summary['commands']} → /solve.<name>")
    for k in ("agents", "skills", "note"):
        if k in summary:
            print(f"  {k:<14} : {summary[k]}")
    print('Next:  solve run "<your problem>" --auto-approve   (or use /solve.mission in your agent)')
    return 0


def _cmd_run(args) -> int:
    from . import runner_bridge
    try:
        out = runner_bridge.run(args.problem, project_root=args.path, auto_approve=args.auto_approve)
    except ModuleNotFoundError as e:
        print(f"error: {e}. `solve run` needs the engine SDK: pip install openai-agents", file=sys.stderr)
        return 2
    print(f"Mission written to: {out}")
    return 0


def _cmd_check(args) -> int:
    ok_all = True
    for label, ok, detail in scaffolder.check(args.path):
        mark = "✓" if ok else "✗"
        ok_all = ok_all and ok
        print(f"  {mark} {label}" + (f"  ({detail})" if detail and not ok else ""))
    return 0 if ok_all else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="solve", description="Solve-Kit — problem-solving toolkit CLI.")
    p.add_argument("--version", action="version", version=f"solve-kit {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("init", help="scaffold .solve/ + agent commands into a project")
    pi.add_argument("path", nargs="?", default=".", help="target project dir (default: .)")
    pi.add_argument("--agent", default="claude", choices=integrations_choices(), help="AI agent integration")
    pi.set_defaults(func=_cmd_init)

    pr = sub.add_parser("run", help="headless mission via the engine (needs openai-agents)")
    pr.add_argument("problem", help="the problem statement")
    pr.add_argument("path", nargs="?", default=".", help="project dir for missions/ output")
    pr.add_argument("--auto-approve", action="store_true", help="non-interactive HITL: auto-GO")
    pr.set_defaults(func=_cmd_run)

    pc = sub.add_parser("check", help="prerequisite / health check")
    pc.add_argument("path", nargs="?", default=".")
    pc.set_defaults(func=_cmd_check)
    return p


def integrations_choices():
    from .integrations import SUPPORTED
    return list(SUPPORTED)


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
