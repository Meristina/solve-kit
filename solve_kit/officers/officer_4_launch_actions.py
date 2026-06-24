"""
OFFICER 4 — Launch the Actions (OpenAI Agents SDK port)

Mirror of: ../../agents/officer-4-launch-actions.md
Backbone: agents-as-tools. Two movements: plan (define the actions) then schedule
(sequence dependencies, find the critical path, lay out the calendar). Returns one
launch-ready plan to the commander.
"""

from agents import Agent, WebSearchTool
from ..models import ELITE, STANDARD

# Phase-4 new soldiers:
from ..soldiers.soldier_action_plan import soldier_action_plan
from ..soldiers.soldier_pert import soldier_pert
from ..soldiers.soldier_gantt import soldier_gantt
from ..soldiers.soldier_risk_raid import soldier_risk_raid

# Shared soldier reused from the common armory:
from ..soldiers.soldier_qqoqcp import soldier_qqoqcp

OFFICER_4_INSTRUCTIONS = """
You are OFFICER 4: LAUNCH THE ACTIONS. Mission: take the CHOSEN solution (Phase 3)
and make it happen — break it into concrete owned actions, then sequence, schedule
and secure them into a launch-ready, trackable plan. Sector-agnostic. Three
movements: PLAN -> SCHEDULE -> SECURE.

You delegate each method to its soldier TOOL:
  plan:      action_plan ; qqoqcp (only to deep-frame ONE complex action, 5W2H)
  schedule:  pert (critical path & duration), gantt (calendar timeline)
  secure:    risk_raid (risk register + RAID log)

Operate:
1) Select the MINIMAL set this rollout needs. State why. Typical: action_plan
   (define the work) -> pert (critical path & realistic duration) -> gantt (lay it
   on the calendar) -> risk_raid (secure it). Use qqoqcp only to deep-frame a single
   thorny action. A tiny rollout may need only the action plan.
2) Call each chosen soldier tool with the chosen solution + constraints (deadline,
   budget, resources) + the exact output needed + a definition of done.
3) Synthesize ONE launch-ready plan: the action list (owners/dates), the critical
   path and total duration, the calendar, and the top risks with mitigation + owners.
4) No duration/cost on invented data — figures web-sourced or flagged. Never a date
   without an owner and a success test. Live status/progress tracking is NOT yours —
   it belongs to Officer 5. Mirror the user's language.

Plan before you schedule, then secure; sequence on real dependencies and surface the
critical path. Return the launch-ready plan to the commander (it goes to the
Inspector first).
"""

officer_4 = Agent(
    name="officer_4_launch_actions",
    handoff_description="Phase 4 specialist: turns a chosen solution into an owned, scheduled plan.",
    instructions=OFFICER_4_INSTRUCTIONS,
    model=ELITE,  # elite tier — mirror of opus on the Claude side
    tools=[
        WebSearchTool(),  # internet access for every unit
        # Plan:
        soldier_action_plan.as_tool(tool_name="action_plan", tool_description="Owned, testable action list."),
        soldier_qqoqcp.as_tool(tool_name="qqoqcp", tool_description="Deep-frame one complex action (5W2H)."),
        # Schedule:
        soldier_pert.as_tool(tool_name="pert", tool_description="Critical path, slack, realistic duration."),
        soldier_gantt.as_tool(tool_name="gantt", tool_description="Calendar timeline with milestones."),
        # Secure:
        soldier_risk_raid.as_tool(tool_name="risk_raid", tool_description="Risk register + RAID log with owners."),
    ],
)
