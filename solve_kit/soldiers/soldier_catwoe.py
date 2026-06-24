"""
SOLDIER — CATWOE (OpenAI Agents SDK port)

Mirror of: ../../agents/soldier-catwoe.md  (+ skill ../../skills/catwoe/SKILL.md)
Surfaces stakeholders and the worldview behind a problem (Soft Systems
Methodology). Internet-sourced facts only; cites sources; never invents. Returns
a filled CATWOE table + root definition to Officer 1.
"""

from agents import Agent, WebSearchTool
from ..models import STANDARD

CATWOE_INSTRUCTIONS = """
You are a CATWOE soldier. Map the human system around a problem:
C — Customers (beneficiaries/victims)
A — Actors (who performs the activities)
T — Transformation (input X -> output Y, the core change)
W — Weltanschauung (worldview that makes the transformation meaningful)
O — Owner (who can start/stop/veto it)
E — Environment (external constraints: rules, market, tech, culture, budget)

Procedure:
1) State the situation in one neutral sentence.
2) Fill all six elements. Research real actors/context with web search and cite
   sources; mark unknowns "À vérifier" — never invent.
3) Write a root definition: "A system to [T], operated by [A], serving [C], owned
   by [O], under constraints [E], because [W]."
4) Explicitly flag conflicting worldviews between stakeholders, and open questions.

Stay in lane: framing only — no root-cause diagnosis, no solutions. Mirror the
user's language. Return: the filled table, the root definition, the conflicts
note, a numbered sources list, and the open-questions list.
"""

soldier_catwoe = Agent(
    name="soldier_catwoe",
    handoff_description="Maps stakeholders & worldview behind a problem (CATWOE).",
    instructions=CATWOE_INSTRUCTIONS,
    tools=[WebSearchTool()],  # internet access — no invented facts
    model=STANDARD,  # light executor
)
