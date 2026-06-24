"""
COMMANDER — Generalist Problem-Solving Army (OpenAI Agents SDK port)

Mirror of: ../agents/commander-problem-solving.md
Backbone: "manager keeps the hand" (agents-as-tools). The commander stays the
owner of the final deliverable; officers are exposed to it via .as_tool().
The Inspector is a mandatory tool called at the end of every loop.

Build order (we add officers/soldiers one by one):
    commander.py            <- this file (head of the chain)
    officers/officer_1_define_problem.py
    soldiers/soldier_qqoqcp.py
    ...
    inspector.py            <- source + compliance + quality gate (veto)

Note: install `openai-agents`. Web access is given to every unit via the SDK's
hosted WebSearchTool so no unit invents facts.

Entry points:
- mission.py  -> the LOOPED, stateful mission (Mission Dossier + iteration cap +
  re-entry on VETO). Use this for real runs; the harness owns the control loop.
- this file's __main__ below is a single-pass demo only.
"""

from agents import Agent, Runner, WebSearchTool
from .models import ELITE

# Officers and inspector are imported as they get built (one per turn).
from .officers.officer_1_define_problem import officer_1
from .officers.officer_2_root_cause import officer_2
from .officers.officer_3_solution import officer_3
from .officers.officer_4_launch_actions import officer_4
from .officers.officer_5_monitor import officer_5
from .inspector import inspector

COMMANDER_INSTRUCTIONS = """
You are the COMMANDER of a generalist, sector-agnostic problem-solving army.
You do not execute methods yourself. You command.

ALWAYS run this doctrine:
0) FRAME: restate the problem in one line; name the sector/context you detected;
   ask 2-3 questions that change the plan, each with a recommended default;
   then WAIT for answers (unless told to "go").
1) DEFINE the problem      -> call tool `define_problem`   (Officer 1)
2) IDENTIFY root causes     -> call tool `identify_causes`  (Officer 2)
3) DESIGN the solution      -> call tool `design_solution`  (Officer 3)
4) LAUNCH the actions       -> call tool `launch_actions`   (Officer 4)
5) MONITOR effectiveness    -> call tool `monitor`          (Officer 5)

Pick the MINIMAL set of phases/tools the problem needs (MECE: no gaps, no
overlap). Justify the selection in one line.

END OF EVERY LOOP: call tool `inspect` (the Inspector). It verifies (a) sources
— every fact must cite a real internet source, nothing invented; (b) compliance
for the detected sector; (c) quality via a devil's-advocate pass that attacks the
unexamined, then converges. The Inspector has veto power: if it flags material
issues, fix and re-inspect before proceeding.

Deliver ONE coherent result, MIRROR THE USER'S LANGUAGE, cite sources, and state
what was verified / changed after critique / still risky.
"""

commander = Agent(
    name="commander",
    instructions=COMMANDER_INSTRUCTIONS,
    model=ELITE,  # elite tier — mirror of opus on the Claude side
    tools=[
        WebSearchTool(),  # every unit can research; the commander too
        officer_1.as_tool(
            tool_name="define_problem",
            tool_description="Phase 1: frame and prioritize the right problem.",
        ),
        officer_2.as_tool(tool_name="identify_causes", tool_description="Phase 2: root causes."),
        officer_3.as_tool(tool_name="design_solution", tool_description="Phase 3: choose a solution."),
        officer_4.as_tool(tool_name="launch_actions",   tool_description="Phase 4: action plan."),
        officer_5.as_tool(tool_name="monitor",          tool_description="Phase 5: monitoring."),
        inspector.as_tool(tool_name="inspect",          tool_description="Sources+compliance+quality gate (veto)."),
    ],
)

if __name__ == "__main__":
    result = Runner.run_sync(commander, "We have a problem: ... (describe it)")
    print(result.final_output)
