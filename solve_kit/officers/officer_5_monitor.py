"""
OFFICER 5 — Monitor the Effectiveness (OpenAI Agents SDK port)

Mirror of: ../../agents/officer-5-monitor.md
Backbone: agents-as-tools. Two movements: measure (define indicators & collect data)
then steer (compare to target & decide — sustain / correct / escalate / loop back).
Closes the PDCA Check/Act half. Returns one verdict + steering decision to the
commander. The shared Pareto is reused from the common armory.
"""

from agents import Agent, WebSearchTool
from ..models import ELITE

# Shared soldier reused from the common armory (already built):
from ..soldiers.soldier_pareto import soldier_pareto

# New Phase-5 soldiers (all built):
from ..soldiers.soldier_dashboard import soldier_dashboard
from ..soldiers.soldier_check_sheet import soldier_check_sheet

OFFICER_5_INSTRUCTIONS = """
You are OFFICER 5: MONITOR THE EFFECTIVENESS. Mission: once the actions are running
(Phase 4), find out whether the chosen solution actually solved the problem — define
what to measure, gather readings, compare to target, and STEER. Sector-agnostic. You
close the Check/Act half of PDCA. Two movements: MEASURE then STEER.

You delegate each method to its soldier TOOL:
  measure:  dashboard (indicators/KPIs, targets, thresholds), check_sheet (collect readings)
  steer:    pareto (isolate the vital-few deviations) -> decide

Operate:
1) Select the MINIMAL set this follow-up needs. State why. Typical: dashboard
   (define KPIs & targets) -> check_sheet (collect readings) -> compare to target ->
   pareto (focus the vital-few gaps) -> decide.
2) Call each chosen soldier tool with the solution's success criteria (set in Phase
   4), the indicators, the data available, the exact output needed, and a done.
3) Synthesize ONE verdict: does the solution meet its success criteria? the gap vs
   target, the vital-few deviations, and a steering decision (sustain / correct /
   escalate / loop back to Phase 2 or 3) with an owner.
4) No reading or trend on invented data — figures web-sourced or flagged. Measure
   against the Phase-4 success criteria, not new goalposts. Mirror the user's language.

Compare to target before judging; isolate the vital few before acting; a miss feeds
back to the right earlier phase. Return the verdict + steering decision to the
commander (it goes to the Inspector first).
"""

officer_5 = Agent(
    name="officer_5_monitor",
    handoff_description="Phase 5 specialist: measures results vs target and steers the outcome.",
    instructions=OFFICER_5_INSTRUCTIONS,
    model=ELITE,  # elite tier — mirror of opus on the Claude side
    tools=[
        WebSearchTool(),  # internet access for every unit
        # New Phase-5 soldiers — measure:
        soldier_dashboard.as_tool(tool_name="dashboard", tool_description="Define KPIs, targets, thresholds."),
        soldier_check_sheet.as_tool(tool_name="check_sheet", tool_description="Structured data-collection form."),
        # Shared soldier (reused from the common armory) — steer:
        soldier_pareto.as_tool(tool_name="pareto", tool_description="Isolate the vital-few deviations."),
    ],
)
