"""
OFFICER 3 — Design the Solution (OpenAI Agents SDK port)

Mirror of: ../../agents/officer-3-solution.md
Backbone: agents-as-tools. Two movements: diverge (generate options) then converge
(evaluate & decide). Returns one justified recommendation to the commander.

Five shared soldiers are reused for free from the common armory — the largest
shared-armory payoff of the whole army.
"""

from agents import Agent, WebSearchTool
from ..models import ELITE, STANDARD

# Shared soldiers reused from the common armory (already built):
from ..soldiers.soldier_brainstorming import soldier_brainstorming
from ..soldiers.soldier_reverse_brainstorming import soldier_reverse_brainstorming
from ..soldiers.soldier_catwoe import soldier_catwoe
from ..soldiers.soldier_circept import soldier_circept
from ..soldiers.soldier_mece import soldier_mece

# New Phase-3 soldiers (all built):
from ..soldiers.soldier_scamper import soldier_scamper
from ..soldiers.soldier_asit import soldier_asit
from ..soldiers.soldier_discovery_matrix import soldier_discovery_matrix
from ..soldiers.soldier_tree_diagram import soldier_tree_diagram
from ..soldiers.soldier_value_analysis import soldier_value_analysis
from ..soldiers.soldier_decision_matrix import soldier_decision_matrix
from ..soldiers.soldier_delphi import soldier_delphi

OFFICER_3_INSTRUCTIONS = """
You are OFFICER 3: DESIGN THE SOLUTION. Mission: from the driving root causes,
generate options, compare them on explicit criteria, and CHOOSE — trade-offs
visible. Sector-agnostic. Two movements: DIVERGE then CONVERGE.

You delegate each method to its soldier TOOL:
  diverge:  brainstorming, reverse_brainstorming, scamper, asit, discovery_matrix,
            circept, catwoe
  converge: tree_diagram, mece, value_analysis, decision_matrix, delphi

Operate:
1) Select the MINIMAL MECE set this case needs. State why. Typical: generate
   (brainstorming/scamper/asit) -> mece (clean the set) -> evaluate
   (decision_matrix or value_analysis) -> choose.
2) Call each chosen soldier tool with root causes + constraints + exact output + done.
3) Synthesize ONE recommendation: chosen solution, why it won (the scoring),
   runner-up, key trade-offs/risks.
4) No option scored on invented data — figures web-sourced or flagged. Mirror the
   user's language.

Diverge before converge; decide on explicit weighted criteria, not gut feel.
Return the recommendation to the commander.
"""

officer_3 = Agent(
    name="officer_3_solution",
    handoff_description="Phase 3 specialist: generates, compares, and chooses a solution.",
    instructions=OFFICER_3_INSTRUCTIONS,
    model=ELITE,  # elite tier — mirror of opus on the Claude side
    tools=[
        WebSearchTool(),  # internet access for every unit
        # New Phase-3 soldiers — diverge then converge:
        soldier_scamper.as_tool(tool_name="scamper", tool_description="Transform an existing solution."),
        soldier_asit.as_tool(tool_name="asit", tool_description="Closed-world constraint invention."),
        soldier_discovery_matrix.as_tool(tool_name="discovery_matrix", tool_description="Cross dimensions for new cells."),
        soldier_tree_diagram.as_tool(tool_name="tree_diagram", tool_description="Means->ends decomposition."),
        soldier_value_analysis.as_tool(tool_name="value_analysis", tool_description="Value = function / cost."),
        soldier_decision_matrix.as_tool(tool_name="decision_matrix", tool_description="Weighted-criteria scoring -> choice."),
        soldier_delphi.as_tool(tool_name="delphi", tool_description="Converge expert opinion when data is scarce."),
        # Shared soldiers (reused from the common armory):
        soldier_brainstorming.as_tool(tool_name="brainstorming", tool_description="Generate candidate solutions."),
        soldier_reverse_brainstorming.as_tool(tool_name="reverse_brainstorming", tool_description="Solutions via inverting failure."),
        soldier_catwoe.as_tool(tool_name="catwoe", tool_description="Re-check vs stakeholders/worldview."),
        soldier_circept.as_tool(tool_name="circept", tool_description="Spark angles via concept opposites."),
        soldier_mece.as_tool(tool_name="mece", tool_description="Keep options/criteria clean."),
    ],
)
