"""
OFFICER 2 — Identify Root Causes (OpenAI Agents SDK port)

Mirror of: ../../agents/officer-2-root-cause.md
Backbone: agents-as-tools. The officer keeps the hand and returns one ranked
root-cause picture to the commander.

Shared soldiers (already built in Phase 1) are reused here for free — this is the
shared-armory payoff. New soldiers get added one by one.
"""

from agents import Agent, WebSearchTool

# Shared soldiers reused from the common armory (already built):
from soldiers.soldier_5_whys import soldier_5_whys
from soldiers.soldier_brainstorming import soldier_brainstorming
from soldiers.soldier_qqoqcp import soldier_qqoqcp

# New Phase-2 soldiers (added one per turn):
from soldiers.soldier_ishikawa import soldier_ishikawa
from soldiers.soldier_relations_diagram import soldier_relations_diagram
from soldiers.soldier_mece import soldier_mece

OFFICER_2_INSTRUCTIONS = """
You are OFFICER 2: IDENTIFY ROOT CAUSES. Mission: move from symptoms to validated,
ranked root causes — never stop at surface explanations. Sector-agnostic. You
receive the defined problem from Phase 1.

You do not run methods yourself; you delegate each to its soldier TOOL:
  ishikawa, relations_diagram, mece (new),
  five_whys, brainstorming, qqoqcp (shared).

Operate:
1) Select the MINIMAL MECE set this case needs. State why in one line. Typical:
   brainstorming (candidate causes) -> ishikawa (structure) -> five_whys (drill
   top branches) -> relations_diagram (driving causes) -> mece (gap/overlap check).
2) Call each chosen soldier tool with the defined problem + exact output + done.
3) Synthesize ONE ranked root-cause picture: causes, evidence, and the DRIVING
   causes (highest leverage).
4) Every cause must be web-sourced or labeled "[hypothèse]" with how to verify.
   Never assert an unproven cause as fact. Mirror the user's language.

Return the ranked root-cause picture to the commander.
"""

officer_2 = Agent(
    name="officer_2_root_cause",
    handoff_description="Phase 2 specialist: finds validated, ranked root causes.",
    instructions=OFFICER_2_INSTRUCTIONS,
    model="gpt-5",  # elite tier — mirror of opus on the Claude side
    tools=[
        WebSearchTool(),  # internet access for every unit
        # New soldiers (uncomment as each is built):
        soldier_ishikawa.as_tool(tool_name="ishikawa", tool_description="5M fishbone cause map."),
        soldier_relations_diagram.as_tool(tool_name="relations_diagram", tool_description="Find driving causes."),
        soldier_mece.as_tool(tool_name="mece", tool_description="No-gap/no-overlap structuring."),
        # Shared soldiers (reused from the common armory):
        soldier_5_whys.as_tool(tool_name="five_whys", tool_description="Drill symptom -> root cause (full)."),
        soldier_brainstorming.as_tool(tool_name="brainstorming", tool_description="Generate candidate causes."),
        soldier_qqoqcp.as_tool(tool_name="qqoqcp", tool_description="Re-pin facts on a cause."),
    ],
)
