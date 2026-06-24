"""
OFFICER 1 — Define the Problem (OpenAI Agents SDK port)

Mirror of: ../../agents/officer-1-define-problem.md
Backbone: agents-as-tools. The officer keeps the hand and exposes each soldier
via .as_tool(). It returns one synthesized problem statement to the commander.
"""

from agents import Agent, WebSearchTool
from ..models import ELITE, STANDARD

# Soldiers are imported as they get built (one per turn).
from ..soldiers.soldier_qqoqcp import soldier_qqoqcp
from ..soldiers.soldier_catwoe import soldier_catwoe
from ..soldiers.soldier_5_whys import soldier_5_whys
from ..soldiers.soldier_brainstorming import soldier_brainstorming
from ..soldiers.soldier_reverse_brainstorming import soldier_reverse_brainstorming
from ..soldiers.soldier_affinity_diagram import soldier_affinity_diagram
from ..soldiers.soldier_circept import soldier_circept
from ..soldiers.soldier_pareto import soldier_pareto

# Shared with Officer 5 — reused here to baseline the CURRENT state of the problem:
from ..soldiers.soldier_check_sheet import soldier_check_sheet
from ..soldiers.soldier_dashboard import soldier_dashboard

OFFICER_1_INSTRUCTIONS = """
You are OFFICER 1: DEFINE THE PROBLEM. Mission: turn a vague situation into a
sharp, scoped, prioritized problem statement (the RIGHT problem) AND a measured
baseline of its current state (the "from what?" Phase 5 will measure against).
Sector-agnostic.

You do not run methods yourself; you delegate each to its soldier TOOL:
  define:    qqoqcp, catwoe, five_whys, brainstorming, reverse_brainstorming,
             affinity_diagram, circept, pareto
  baseline:  check_sheet (capture current-state readings), dashboard (quantify the
             current state as indicators) — both shared with Officer 5

Operate:
1) Select the MINIMAL MECE set of soldier tools this problem needs (not all).
   State in one line why.
2) Call each chosen soldier tool with the situation + exact output needed +
   definition of done.
3) BASELINE: when the problem is quantifiable, deploy check_sheet/dashboard to
   capture the current state (value + when + source). If it's not quantifiable or
   there's no data yet, say so explicitly — don't fabricate a number.
4) Synthesize ONE problem statement: what it is, scope (in/out), stakeholders,
   priority/severity, AND the baseline (or "not quantifiable / no data yet").
5) Every factual claim must cite a real internet source (use web search). Never
   invent data. Flag open questions. Mirror the user's language.

Return the synthesized problem statement + baseline to the commander (it seeds the
Mission Dossier's `baseline`).
"""

officer_1 = Agent(
    name="officer_1_define_problem",
    handoff_description="Phase 1 specialist: frames and prioritizes the right problem.",
    instructions=OFFICER_1_INSTRUCTIONS,
    model=ELITE,  # elite tier — mirror of opus on the Claude side
    tools=[
        WebSearchTool(),  # internet access for every unit
        soldier_qqoqcp.as_tool(
            tool_name="qqoqcp",
            tool_description="Pin down facts: Who/What/Where/When/How/How-much/Why.",
        ),
        soldier_catwoe.as_tool(tool_name="catwoe", tool_description="Stakeholders & worldview."),
        soldier_5_whys.as_tool(tool_name="five_whys", tool_description="Drill symptom -> issue."),
        soldier_brainstorming.as_tool(tool_name="brainstorming", tool_description="Diverge framings."),
        soldier_reverse_brainstorming.as_tool(tool_name="reverse_brainstorming", tool_description="Invert the problem."),
        soldier_affinity_diagram.as_tool(tool_name="affinity_diagram", tool_description="Cluster inputs into themes."),
        soldier_circept.as_tool(tool_name="circept", tool_description="Map concept & opposites."),
        soldier_pareto.as_tool(tool_name="pareto", tool_description="Prioritize 20/80."),
        # Baseline (shared with Officer 5 — measure the current problem state):
        soldier_check_sheet.as_tool(tool_name="check_sheet", tool_description="Capture current-state readings."),
        soldier_dashboard.as_tool(tool_name="dashboard", tool_description="Quantify current state as indicators."),
    ],
)
